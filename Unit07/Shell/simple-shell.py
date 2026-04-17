#!/usr/bin/env python3
"""
SimpleShell - A basic command-line interface implementation

This module provides a simple shell environment with basic commands like
LIST (directory listing), ADD (number addition), HELP (command help),
and EXIT (quit shell). This implementation serves as an educational
example and should not be used in production without proper security
enhancements.
"""

import os
import sys

class SimpleShell:
    """
    A simple shell implementation with basic command functionality.

    This class provides a command-line interface with a set of basic commands.
    It demonstrates fundamental concepts of shell design including command
    parsing, execution, and error handling.

    Attributes:
        commands (dict): Dictionary mapping command names to their handler functions
        running (bool): Flag indicating if the shell is currently running
    """

    def __init__(self):
        """
        Initialize the shell with available commands.
        
        Sets up the command dictionary and running state. Each command is mapped
        to its corresponding method in the class.
        """
        self.commands = {
            'LIST': self.list_directory,
            'ADD': self.add_numbers,
            'HELP': self.show_help,
            'EXIT': self.exit_shell
        }
        self.running = True

    def list_directory(self, *args):
        """
        List contents of the current directory.

        Args:
            *args: Variable length argument list (unused in this method)

        Returns:
            None

        Raises:
            Exception: If there's an error accessing the directory
        """
        try:
            # Get and display directory contents
            contents = os.listdir('.')
            for item in contents:
                print(item)
        except Exception as e:
            print(f"Error listing directory: {e}")

    def add_numbers(self, *args):
        """
        Add two numbers provided as command arguments.

        Args:
            *args: Variable length argument list, expects exactly two numeric values

        Returns:
            None

        Raises:
            ValueError: If the arguments cannot be converted to numbers
        """
        try:
            # Validate number of arguments
            if len(args) != 2:
                print("Usage: ADD number1 number2")
                return
            
            # Convert arguments to float and calculate sum
            num1 = float(args[0])
            num2 = float(args[1])
            print(f"Result: {num1 + num2}")
        except ValueError:
            print("Error: Please provide valid numbers")

    def show_help(self, *args):
        """
        Display available commands and their usage.

        Args:
            *args: Variable length argument list (unused in this method)

        Returns:
            None
        """
        print("\nAvailable commands:")
        print("  LIST  - List contents of current directory")
        print("  ADD   - Add two numbers (Usage: ADD number1 number2)")
        print("  HELP  - Show this help message")
        print("  EXIT  - Exit the shell\n")

    def exit_shell(self, *args):
        """
        Exit the shell by setting the running flag to False.

        Args:
            *args: Variable length argument list (unused in this method)

        Returns:
            None
        """
        self.running = False
        print("Goodbye!")

    def run(self):
        """
        Main shell loop that processes user input and executes commands.

        This method continuously prompts for user input, parses commands,
        and executes the corresponding command handlers until the EXIT
        command is given or the shell is interrupted.

        Returns:
            None
        """
        print("Welcome to SimpleShell! Type HELP for available commands.")
        
        while self.running:
            try:
                # Get user input and remove leading/trailing whitespace
                command_line = input('shell> ').strip()
                
                # Skip empty commands
                if not command_line:
                    continue
                
                # Parse command and arguments
                # Split input into command and args, convert command to uppercase
                parts = command_line.split()
                command = parts[0].upper()  # Command is case-insensitive
                args = parts[1:]  # All remaining parts are arguments
                
                # Execute command if it exists in the commands dictionary
                if command in self.commands:
                    self.commands[command](*args)
                else:
                    print(f"Unknown command: {command}")
                    print("Type HELP for available commands")
                    
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\nUse EXIT to quit the shell")
            except Exception as e:
                # Catch and display any other errors
                print(f"Error: {e}")

# Entry point of the program
if __name__ == "__main__":
    shell = SimpleShell()
    shell.run()
