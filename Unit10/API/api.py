"""
Unit 10 - API Demonstration
Secure Retail Shop - Order Payment Endpoint (Stripe sandbox)

This module extends the Unit 7 tutorial API (flask_restful User resource)
with a single endpoint drawn from the summative retail-shop assessment:
a sandbox payment call that the storefront makes against the Stripe
test API when a customer confirms their order.

If the stripe Python library is installed and a test secret key is
exported in STRIPE_SECRET_KEY (prefix "sk_test_"), the endpoint calls
the real Stripe sandbox. Otherwise it falls back to a deterministic
local simulator so the demonstration remains runnable without network
access or an account.

The endpoint design follows the 12 RESTful design rules empirically
validated by Bogner, Kotstein and Pfaff (2023); see the accompanying
PDF write-up for a discussion.

Run:
    export STRIPE_SECRET_KEY="sk_test_..."   # optional
    python api.py
"""

import logging
import os
import re
import uuid

from flask import Flask
from flask_restful import Api, Resource, reqparse

try:
    import stripe  
except ImportError:
    stripe = None  


# ---------------------------------------------------------------------------
# Application bootstrap
# ---------------------------------------------------------------------------

app = Flask(__name__)
api = Api(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("shop.log"), logging.StreamHandler()],
)
logger = logging.getLogger("retail-shop.api")

# Secrets are read from the environment. Committing keys to source
# control would be the single worst defect in a "secure" retail shop.
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")

STRIPE_ENABLED = False
if stripe is not None and STRIPE_SECRET_KEY.startswith("sk_test_"):
    stripe.api_key = STRIPE_SECRET_KEY
    STRIPE_ENABLED = True
    logger.info("Stripe sandbox enabled")
else:
    logger.info("Stripe sandbox not configured - using local simulator")


# ---------------------------------------------------------------------------
# Unit 7 resource kept intact (extension, not replacement)
# ---------------------------------------------------------------------------

users = [
    {"name": "James", "age": 30, "occupation": "Network Engineer"},
    {"name": "Ann", "age": 32, "occupation": "Doctor"},
    {"name": "Jason", "age": 22, "occupation": "Web Developer"},
]


class User(Resource):
    """Unchanged from Unit 7 so existing tutorial tests keep passing."""

    def get(self, name):
        for user in users:
            if name == user["name"]:
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if name == user["name"]:
                return f"User with name {name} already exists", 400

        user = {"name": name, "age": args["age"], "occupation": args["occupation"]}
        users.append(user)
        return user, 201


api.add_resource(User, "/user/<string:name>")


# ---------------------------------------------------------------------------
# Unit 10 extension - Order payment via Stripe sandbox
# ---------------------------------------------------------------------------
#
# The summative Secure Retail Shop lets a customer place an order and
# then pay for it. The payment call is delegated to Stripe's test API
# so that no real card data touches the application; the shop only
# forwards a payment-method token created by Stripe.js in the browser.
#
# In-memory order ledger - in the real system this is a relational
# table guarded by a parameterised query and a row-level lock.

orders = {
    "ord_1001": {"id": "ord_1001", "amount": 4999, "currency": "gbp", "status": "pending"},
    "ord_1002": {"id": "ord_1002", "amount": 12500, "currency": "eur", "status": "pending"},
    "ord_1003": {"id": "ord_1003", "amount": 850, "currency": "usd", "status": "pending"},
}

ORDER_ID_PATTERN = re.compile(r"^ord_[0-9]{3,}$")

# Accept only test payment-method tokens. The real PSP would reject
# anything else, but short-circuiting here gives us a clear 400 and a
# safe log line rather than a noisy upstream error.
PAYMENT_METHOD_PATTERN = re.compile(r"^pm_[a-zA-Z0-9_]+$")


class OrderPayment(Resource):
    """
    Payment sub-resource of an order.

    URI template:
        POST /api/v1/orders/<order_id>/payments
        Headers: Idempotency-Key: <uuid4>
        Body:    { "payment_method": "pm_card_visa" }

    Design choices (Bogner, Kotstein and Pfaff, 2023):
      - Plural nouns for both the parent (orders) and child (payments)
        collections.
      - Payment modelled as a sub-resource rather than a verb (no /pay
        or /charge in the path).
      - HTTP verb conveys the operation: POST creates a new payment
        attempt, so the path itself is free of action words.
      - Lowercase letters, underscore only inside identifiers, version
        segment immediately after the API root.
      - Explicit status codes for every outcome, including 402 Payment
        Required for upstream declines and 409 Conflict for duplicates.
    """

    def post(self, order_id: str):
        normalised_id = order_id.strip().lower()

        if not ORDER_ID_PATTERN.match(normalised_id):
            logger.warning("Rejected payment - invalid order id format")
            return {"error": "Invalid order id format"}, 400

        order = orders.get(normalised_id)
        if order is None:
            logger.info("Payment - order not found")
            return {"error": "Order not found"}, 404

        if order["status"] == "paid":
            # 409 Conflict rather than a silent 200: retry loops on the
            # client side are a common source of duplicate charges, and
            # an explicit conflict response makes the bug easy to spot.
            logger.info("Payment - order already paid")
            return {"error": "Order already paid", "order_id": order["id"]}, 409

        parser = reqparse.RequestParser()
        parser.add_argument("payment_method", type=str, required=True, location="json")
        parser.add_argument(
            "Idempotency-Key",
            type=str,
            location="headers",
            dest="idempotency_key",
            required=False,
        )
        args = parser.parse_args()

        payment_method = (args["payment_method"] or "").strip()
        if not PAYMENT_METHOD_PATTERN.match(payment_method):
            logger.warning("Rejected payment - invalid payment_method format")
            return {"error": "Invalid payment_method format"}, 400

        # Generate an idempotency key if the client did not supply one.
        # This still prevents accidental double-charges on a single
        # Flask retry, though a well-behaved client should always send
        # its own key.
        idempotency_key = args.get("idempotency_key") or str(uuid.uuid4())

        # Structured log line - note that the payment-method token and
        # the idempotency key are deliberately NOT logged.
        logger.info(
            "Payment attempt - order=%s amount=%s currency=%s",
            order["id"],
            order["amount"],
            order["currency"],
        )

        if STRIPE_ENABLED:
            try:
                intent = stripe.PaymentIntent.create(
                    amount=order["amount"],
                    currency=order["currency"],
                    payment_method=payment_method,
                    confirm=True,
                    automatic_payment_methods={
                        "enabled": True,
                        "allow_redirects": "never",
                    },
                    metadata={"order_id": order["id"]},
                    idempotency_key=idempotency_key,
                )
                payment_status = intent.status
                payment_id = intent.id
            except stripe.error.CardError as e:  # type: ignore[attr-defined]
                logger.info("Payment declined by PSP - code=%s", e.code)
                return {"error": "Payment declined", "code": e.code}, 402
            except stripe.error.StripeError as e:  # type: ignore[attr-defined]
                logger.error("PSP error - code=%s", getattr(e, "code", "unknown"))
                return {"error": "Upstream payment service error"}, 502
        else:
            # Deterministic local simulator. pm_card_visa succeeds,
            # pm_card_chargeDeclined mirrors Stripe's named decline
            # fixture, anything else is treated as requires_action.
            simulated = {
                "pm_card_visa": "succeeded",
                "pm_card_visa_debit": "succeeded",
                "pm_card_mastercard": "succeeded",
                "pm_card_chargeDeclined": "requires_payment_method",
            }
            payment_status = simulated.get(payment_method, "requires_action")
            payment_id = f"pi_sim_{uuid.uuid4().hex[:16]}"

        if payment_status == "succeeded":
            order["status"] = "paid"
            logger.info("Payment succeeded - order=%s", order["id"])
            return {
                "order_id": order["id"],
                "payment_id": payment_id,
                "status": payment_status,
                "amount": order["amount"],
                "currency": order["currency"],
            }, 201

        logger.info("Payment not completed - order=%s status=%s", order["id"], payment_status)
        return {
            "order_id": order["id"],
            "payment_id": payment_id,
            "status": payment_status,
        }, 402


api.add_resource(OrderPayment, "/api/v1/orders/<string:order_id>/payments")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # debug=False so the Werkzeug debugger PIN is never exposed, which
    # aligns with the secure-by-default posture of the summative design.
    app.run(host="127.0.0.1", port=5000, debug=False)
