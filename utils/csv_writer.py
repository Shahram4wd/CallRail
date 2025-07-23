"""
CSV writing utilities for CallRail data extractor.
"""
import csv
import os
import pandas as pd
from typing import List, Dict, Any, Optional
from config.settings import settings
from utils.logger import logger


class CSVWriter:
    """Handles CSV file writing operations."""
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or settings.output.data_directory
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Ensure the output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")
    
    def write_records(self, endpoint_name: str, records: List[Dict[str, Any]], 
                     fieldnames: Optional[List[str]] = None) -> str:
        """Write records to a CSV file."""
        if not records:
            logger.warning(f"No records to write for endpoint: {endpoint_name}")
            return ""
        
        filename = f"{endpoint_name}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        # Determine fieldnames if not provided
        if not fieldnames:
            fieldnames = self._get_all_fieldnames(records)
        
        try:
            with open(filepath, 'w', newline='', encoding=settings.output.csv_encoding) as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=fieldnames,
                    delimiter=settings.output.csv_delimiter,
                    quoting=csv.QUOTE_MINIMAL,
                    extrasaction='ignore'
                )
                
                if settings.output.include_headers:
                    writer.writeheader()
                
                for record in records:
                    # Flatten nested dictionaries and handle None values
                    flattened_record = self._flatten_record(record)
                    writer.writerow(flattened_record)
            
            logger.info(f"Successfully wrote {len(records)} records to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error writing CSV file {filepath}: {str(e)}")
            raise
    
    def append_records(self, endpoint_name: str, records: List[Dict[str, Any]], 
                      fieldnames: Optional[List[str]] = None) -> str:
        """Append records to an existing CSV file."""
        if not records:
            return ""
        
        filename = f"{endpoint_name}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        # Check if file exists to determine if we need headers
        file_exists = os.path.exists(filepath)
        
        # Determine fieldnames if not provided
        if not fieldnames:
            if file_exists:
                fieldnames = self._get_existing_fieldnames(filepath)
            else:
                fieldnames = self._get_all_fieldnames(records)
        
        try:
            mode = 'a' if file_exists else 'w'
            with open(filepath, mode, newline='', encoding=settings.output.csv_encoding) as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=fieldnames,
                    delimiter=settings.output.csv_delimiter,
                    quoting=csv.QUOTE_MINIMAL,
                    extrasaction='ignore'
                )
                
                # Write headers only if file is new
                if not file_exists and settings.output.include_headers:
                    writer.writeheader()
                
                for record in records:
                    flattened_record = self._flatten_record(record)
                    writer.writerow(flattened_record)
            
            action = "appended to" if file_exists else "created"
            logger.info(f"Successfully {action} {filepath} with {len(records)} records")
            return filepath
            
        except Exception as e:
            logger.error(f"Error writing CSV file {filepath}: {str(e)}")
            raise
    
    def write_with_pandas(self, endpoint_name: str, records: List[Dict[str, Any]]) -> str:
        """Write records using pandas for better performance with large datasets."""
        if not records:
            logger.warning(f"No records to write for endpoint: {endpoint_name}")
            return ""
        
        filename = f"{endpoint_name}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(records)
            
            # Flatten nested columns
            df = self._flatten_dataframe(df)
            
            # Write to CSV
            df.to_csv(
                filepath,
                index=False,
                encoding=settings.output.csv_encoding,
                sep=settings.output.csv_delimiter
            )
            
            logger.info(f"Successfully wrote {len(records)} records to {filepath} using pandas")
            return filepath
            
        except Exception as e:
            logger.error(f"Error writing CSV file {filepath} with pandas: {str(e)}")
            raise
    
    def _get_all_fieldnames(self, records: List[Dict[str, Any]]) -> List[str]:
        """Extract all unique fieldnames from records."""
        fieldnames = set()
        for record in records:
            flattened = self._flatten_record(record)
            fieldnames.update(flattened.keys())
        return sorted(list(fieldnames))
    
    def _get_existing_fieldnames(self, filepath: str) -> List[str]:
        """Get fieldnames from existing CSV file."""
        try:
            with open(filepath, 'r', encoding=settings.output.csv_encoding) as csvfile:
                reader = csv.reader(csvfile, delimiter=settings.output.csv_delimiter)
                return next(reader)
        except Exception as e:
            logger.error(f"Error reading existing CSV headers from {filepath}: {str(e)}")
            return []
    
    def _flatten_record(self, record: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """Flatten nested dictionaries in a record."""
        items = []
        for key, value in record.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                items.extend(self._flatten_record(value, new_key, sep=sep).items())
            elif isinstance(value, list):
                # Convert lists to comma-separated strings
                if value and isinstance(value[0], dict):
                    # For list of dicts, convert to JSON-like string
                    items.append((new_key, str(value)))
                else:
                    # For simple lists, join with commas
                    items.append((new_key, ', '.join(map(str, value)) if value else ''))
            else:
                # Handle None values and convert to string
                items.append((new_key, str(value) if value is not None else ''))
        
        return dict(items)
    
    def _flatten_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flatten nested columns in a DataFrame."""
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if column contains dictionaries
                sample_value = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
                if isinstance(sample_value, dict):
                    # Flatten dictionary columns
                    flattened = pd.json_normalize(df[col].dropna())
                    flattened.index = df[col].dropna().index
                    
                    # Add flattened columns with prefix
                    for flat_col in flattened.columns:
                        df[f"{col}_{flat_col}"] = flattened[flat_col]
                    
                    # Drop original column
                    df = df.drop(columns=[col])
                elif isinstance(sample_value, list):
                    # Convert lists to strings
                    df[col] = df[col].apply(
                        lambda x: ', '.join(map(str, x)) if isinstance(x, list) and x else str(x) if x is not None else ''
                    )
        
        return df
    
    def get_file_info(self, endpoint_name: str) -> Dict[str, Any]:
        """Get information about a CSV file."""
        filename = f"{endpoint_name}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        if not os.path.exists(filepath):
            return {'exists': False}
        
        try:
            file_size = os.path.getsize(filepath)
            
            # Count rows
            with open(filepath, 'r', encoding=settings.output.csv_encoding) as csvfile:
                reader = csv.reader(csvfile)
                row_count = sum(1 for row in reader)
                if settings.output.include_headers and row_count > 0:
                    row_count -= 1  # Subtract header row
            
            return {
                'exists': True,
                'filepath': filepath,
                'size_bytes': file_size,
                'size_mb': round(file_size / (1024 * 1024), 2),
                'row_count': row_count
            }
            
        except Exception as e:
            logger.error(f"Error getting file info for {filepath}: {str(e)}")
            return {'exists': True, 'error': str(e)}


# Global CSV writer instance
csv_writer = CSVWriter()
