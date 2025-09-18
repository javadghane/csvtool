#!/usr/bin/env python3
"""
csvtool - A command-line tool for working with CSV files
Enhanced with default readable mode for piped input
"""

import argparse
import csv
import sys
import re
import os
from io import StringIO


class CSVTool:
    def __init__(self):
        self.delimiter = ','
        self.quote_char = '"'
        
    def read_csv(self, input_source, has_header=True):
        """Read CSV data from file or stdin"""
        if isinstance(input_source, str):
            if input_source == '-':
                content = sys.stdin.read()
            else:
                with open(input_source, 'r', encoding='utf-8') as f:
                    content = f.read()
        else:
            content = input_source.read()
            
        reader = csv.reader(StringIO(content), delimiter=self.delimiter, quotechar=self.quote_char)
        rows = list(reader)
        
        if has_header and rows:
            return rows[0], rows[1:]
        else:
            return None, rows
    
    def write_csv(self, headers, rows, output=None):
        """Write CSV data to output"""
        if output is None:
            output = sys.stdout
            
        writer = csv.writer(output, delimiter=self.delimiter, quotechar=self.quote_char, quoting=csv.QUOTE_MINIMAL)
        
        if headers:
            writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
    
    def readable(self, input_source, no_header=False):
        """Display CSV in readable format"""
        headers, rows = self.read_csv(input_source, has_header=not no_header)
        
        if not rows and not headers:
            return
            
        all_rows = []
        if headers and not no_header:
            all_rows.append(headers)
        all_rows.extend(rows)
        
        if not all_rows:
            return
            
        # Calculate column widths
        widths = []
        for col_idx in range(len(all_rows[0])):
            max_width = 0
            for row in all_rows:
                if col_idx < len(row):
                    max_width = max(max_width, len(str(row[col_idx])))
            widths.append(max_width)
        
        # Print formatted output
        for row_idx, row in enumerate(all_rows):
            formatted_row = []
            for col_idx, cell in enumerate(row):
                if col_idx < len(widths):
                    formatted_row.append(str(cell).ljust(widths[col_idx]))
                else:
                    formatted_row.append(str(cell))
            print(' | '.join(formatted_row))
            
            # Print separator after header
            if row_idx == 0 and headers and not no_header:
                separator = []
                for width in widths:
                    separator.append('-' * width)
                print('-|-'.join(separator))
    
    def select_columns(self, input_source, columns, no_header=False):
        """Select specific columns"""
        headers, rows = self.read_csv(input_source, has_header=not no_header)
        
        # Parse column indices
        col_indices = []
        for col in columns.split(','):
            col = col.strip()
            if col.isdigit():
                col_indices.append(int(col) - 1)  # Convert to 0-based index
            else:
                # Handle column names
                if headers:
                    try:
                        col_indices.append(headers.index(col))
                    except ValueError:
                        print(f"Column '{col}' not found", file=sys.stderr)
                        sys.exit(1)
        
        # Select columns from headers
        new_headers = None
        if headers and not no_header:
            new_headers = [headers[i] for i in col_indices if i < len(headers)]
        
        # Select columns from rows
        new_rows = []
        for row in rows:
            new_row = []
            for i in col_indices:
                if i < len(row):
                    new_row.append(row[i])
                else:
                    new_row.append('')
            new_rows.append(new_row)
        
        self.write_csv(new_headers, new_rows)
    
    def search(self, input_source, column, pattern, no_header=False):
        """Search for pattern in specified column"""
        headers, rows = self.read_csv(input_source, has_header=not no_header)
        
        # Parse column index
        if column.isdigit():
            col_index = int(column) - 1
        else:
            if headers:
                try:
                    col_index = headers.index(column)
                except ValueError:
                    print(f"Column '{column}' not found", file=sys.stderr)
                    sys.exit(1)
            else:
                print("Cannot use column name without headers", file=sys.stderr)
                sys.exit(1)
        
        # Filter rows
        filtered_rows = []
        for row in rows:
            if col_index < len(row):
                if re.search(pattern, str(row[col_index])):
                    filtered_rows.append(row)
        
        self.write_csv(headers if not no_header else None, filtered_rows)
    
    def replace(self, input_source, column, old_value, new_value, no_header=False):
        """Replace values in specified column"""
        headers, rows = self.read_csv(input_source, has_header=not no_header)
        
        # Parse column index
        if column.isdigit():
            col_index = int(column) - 1
        else:
            if headers:
                try:
                    col_index = headers.index(column)
                except ValueError:
                    print(f"Column '{column}' not found", file=sys.stderr)
                    sys.exit(1)
            else:
                print("Cannot use column name without headers", file=sys.stderr)
                sys.exit(1)
        
        # Replace values
        for row in rows:
            if col_index < len(row):
                if str(row[col_index]) == old_value:
                    row[col_index] = new_value
        
        self.write_csv(headers if not no_header else None, rows)


def is_piped_input():
    """Check if input is coming from a pipe"""
    return not sys.stdin.isatty()


def main():
    parser = argparse.ArgumentParser(
        description='CSV manipulation tool with default readable mode for piped input',
        prog='csvtool'
    )
    
    # Check for default behavior (no arguments + piped input)
    if len(sys.argv) == 1 and is_piped_input():
        # Default behavior: readable mode from stdin
        tool = CSVTool()
        tool.readable('-')
        return
    
    # Global options
    parser.add_argument('--no-header', action='store_true',
                       help='Treat first row as data, not header')
    parser.add_argument('--delimiter', '-d', default=',',
                       help='Field delimiter (default: comma)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Readable command
    readable_parser = subparsers.add_parser('readable', help='Display CSV in readable format')
    readable_parser.add_argument('file', nargs='?', default='-',
                               help='CSV file to read (default: stdin)')
    
    # Select columns command
    select_parser = subparsers.add_parser('select', help='Select specific columns')
    select_parser.add_argument('-c', '--columns', required=True,
                             help='Comma-separated column indices or names')
    select_parser.add_argument('file', nargs='?', default='-',
                             help='CSV file to read (default: stdin)')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for pattern in column')
    search_parser.add_argument('-c', '--column', required=True,
                             help='Column index or name to search in')
    search_parser.add_argument('-s', '--search', required=True,
                             help='Search pattern (regex supported)')
    search_parser.add_argument('file', nargs='?', default='-',
                             help='CSV file to read (default: stdin)')
    
    # Replace command
    replace_parser = subparsers.add_parser('replace', help='Replace values in column')
    replace_parser.add_argument('-c', '--column', required=True,
                              help='Column index or name')
    replace_parser.add_argument('-o', '--old', required=True,
                              help='Old value to replace')
    replace_parser.add_argument('-n', '--new', required=True,
                              help='New value')
    replace_parser.add_argument('file', nargs='?', default='-',
                              help='CSV file to read (default: stdin)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command specified and no piped input, show help
    if not args.command and not is_piped_input():
        parser.print_help()
        return
    
    # Initialize tool
    tool = CSVTool()
    tool.delimiter = args.delimiter
    
    # Execute command
    if args.command == 'readable':
        tool.readable(args.file, args.no_header)
    elif args.command == 'select':
        tool.select_columns(args.file, args.columns, args.no_header)
    elif args.command == 'search':
        tool.search(args.file, args.column, args.search, args.no_header)
    elif args.command == 'replace':
        tool.replace(args.file, args.column, args.old, args.new, args.no_header)
    elif not args.command and is_piped_input():
        # This should have been caught earlier, but just in case
        tool.readable('-')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        # Handle broken pipe gracefully
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)
