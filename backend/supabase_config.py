#!/usr/bin/env python3
"""
Supabase Configuration Helper
Provides utilities for connecting to and querying Supabase
"""

import os
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv('/home/claude-user/ai-consults-platform/00-pivot/.env')

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
SUPABASE_PUBLIC_ANON = os.getenv('SUPABASE_PUBLIC_ANON')

# API Endpoints
SUPABASE_API_URL = f"{SUPABASE_URL}/rest/v1"
SUPABASE_AUTH_URL = f"{SUPABASE_URL}/auth/v1"


class SupabaseClient:
    """
    Simple Supabase REST API client
    """

    def __init__(self, use_service_key: bool = True):
        """
        Initialize Supabase client

        Args:
            use_service_key: If True, use service key (admin). If False, use anon key (public)
        """
        self.api_key = SUPABASE_SERVICE_KEY if use_service_key else SUPABASE_PUBLIC_ANON
        self.base_url = SUPABASE_API_URL
        self.headers = {
            'apikey': self.api_key,
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def table(self, table_name: str):
        """
        Get a table query builder

        Args:
            table_name: Name of the table to query

        Returns:
            TableQuery instance
        """
        return TableQuery(self, table_name)

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make HTTP request to Supabase API

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            url: Request URL
            **kwargs: Additional request parameters

        Returns:
            requests.Response
        """
        headers = kwargs.pop('headers', {})
        headers.update(self.headers)

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            timeout=kwargs.pop('timeout', 30),
            **kwargs
        )

        return response


class TableQuery:
    """
    Table query builder for Supabase REST API
    """

    def __init__(self, client: SupabaseClient, table_name: str):
        self.client = client
        self.table_name = table_name
        self.url = f"{client.base_url}/{table_name}"
        self.params = {}
        self.prefer_headers = []

    def select(self, columns: str = "*") -> 'TableQuery':
        """
        Select columns to return

        Args:
            columns: Comma-separated column names or "*" for all

        Returns:
            self for chaining
        """
        self.params['select'] = columns
        return self

    def eq(self, column: str, value: Any) -> 'TableQuery':
        """
        Filter where column equals value

        Args:
            column: Column name
            value: Value to match

        Returns:
            self for chaining
        """
        self.params[column] = f"eq.{value}"
        return self

    def neq(self, column: str, value: Any) -> 'TableQuery':
        """
        Filter where column does not equal value

        Args:
            column: Column name
            value: Value to exclude

        Returns:
            self for chaining
        """
        self.params[column] = f"neq.{value}"
        return self

    def gt(self, column: str, value: Any) -> 'TableQuery':
        """
        Filter where column is greater than value

        Args:
            column: Column name
            value: Minimum value (exclusive)

        Returns:
            self for chaining
        """
        self.params[column] = f"gt.{value}"
        return self

    def gte(self, column: str, value: Any) -> 'TableQuery':
        """
        Filter where column is greater than or equal to value

        Args:
            column: Column name
            value: Minimum value (inclusive)

        Returns:
            self for chaining
        """
        self.params[column] = f"gte.{value}"
        return self

    def lt(self, column: str, value: Any) -> 'TableQuery':
        """
        Filter where column is less than value

        Args:
            column: Column name
            value: Maximum value (exclusive)

        Returns:
            self for chaining
        """
        self.params[column] = f"lt.{value}"
        return self

    def lte(self, column: str, value: Any) -> 'TableQuery':
        """
        Filter where column is less than or equal to value

        Args:
            column: Column name
            value: Maximum value (inclusive)

        Returns:
            self for chaining
        """
        self.params[column] = f"lte.{value}"
        return self

    def like(self, column: str, pattern: str) -> 'TableQuery':
        """
        Filter where column matches pattern (case-sensitive)

        Args:
            column: Column name
            pattern: SQL LIKE pattern

        Returns:
            self for chaining
        """
        self.params[column] = f"like.{pattern}"
        return self

    def ilike(self, column: str, pattern: str) -> 'TableQuery':
        """
        Filter where column matches pattern (case-insensitive)

        Args:
            column: Column name
            pattern: SQL LIKE pattern

        Returns:
            self for chaining
        """
        self.params[column] = f"ilike.{pattern}"
        return self

    def in_(self, column: str, values: List[Any]) -> 'TableQuery':
        """
        Filter where column is in list of values

        Args:
            column: Column name
            values: List of values to match

        Returns:
            self for chaining
        """
        formatted_values = ','.join(str(v) for v in values)
        self.params[column] = f"in.({formatted_values})"
        return self

    def order(self, column: str, ascending: bool = True) -> 'TableQuery':
        """
        Order results by column

        Args:
            column: Column name to order by
            ascending: If True, ascending order. If False, descending

        Returns:
            self for chaining
        """
        order_str = column if ascending else f"{column}.desc"
        self.params['order'] = order_str
        return self

    def limit(self, count: int) -> 'TableQuery':
        """
        Limit number of results

        Args:
            count: Maximum number of results

        Returns:
            self for chaining
        """
        self.params['limit'] = count
        return self

    def offset(self, count: int) -> 'TableQuery':
        """
        Offset results (for pagination)

        Args:
            count: Number of results to skip

        Returns:
            self for chaining
        """
        self.params['offset'] = count
        return self

    def count(self, count_type: str = "exact") -> 'TableQuery':
        """
        Get count of results

        Args:
            count_type: Type of count - "exact", "planned", or "estimated"

        Returns:
            self for chaining
        """
        self.prefer_headers.append(f"count={count_type}")
        return self

    def execute(self) -> Dict[str, Any]:
        """
        Execute the query

        Returns:
            Dict with 'data' and optional 'count'
        """
        headers = {}
        if self.prefer_headers:
            headers['Prefer'] = ','.join(self.prefer_headers)

        response = self.client._request(
            method='GET',
            url=self.url,
            params=self.params,
            headers=headers
        )

        result = {
            'data': response.json() if response.status_code in [200, 206] else None,
            'status_code': response.status_code
        }

        # Extract count from Content-Range header if present
        content_range = response.headers.get('Content-Range')
        if content_range:
            try:
                result['count'] = int(content_range.split('/')[1])
            except (IndexError, ValueError):
                pass

        return result

    def insert(self, data: Dict[str, Any], return_representation: bool = True) -> Dict[str, Any]:
        """
        Insert new row(s)

        Args:
            data: Dictionary or list of dictionaries to insert
            return_representation: If True, return inserted data

        Returns:
            Dict with 'data' and 'status_code'
        """
        headers = {}
        if return_representation:
            headers['Prefer'] = 'return=representation'
        else:
            headers['Prefer'] = 'return=minimal'

        response = self.client._request(
            method='POST',
            url=self.url,
            json=data,
            headers=headers
        )

        return {
            'data': response.json() if return_representation and response.status_code in [200, 201] else None,
            'status_code': response.status_code
        }

    def update(self, data: Dict[str, Any], return_representation: bool = True) -> Dict[str, Any]:
        """
        Update row(s) matching current filters

        Args:
            data: Dictionary of fields to update
            return_representation: If True, return updated data

        Returns:
            Dict with 'data' and 'status_code'
        """
        headers = {}
        if return_representation:
            headers['Prefer'] = 'return=representation'
        else:
            headers['Prefer'] = 'return=minimal'

        response = self.client._request(
            method='PATCH',
            url=self.url,
            params=self.params,
            json=data,
            headers=headers
        )

        return {
            'data': response.json() if return_representation and response.status_code == 200 else None,
            'status_code': response.status_code
        }

    def delete(self, return_representation: bool = False) -> Dict[str, Any]:
        """
        Delete row(s) matching current filters

        Args:
            return_representation: If True, return deleted data

        Returns:
            Dict with 'data' and 'status_code'
        """
        headers = {}
        if return_representation:
            headers['Prefer'] = 'return=representation'
        else:
            headers['Prefer'] = 'return=minimal'

        response = self.client._request(
            method='DELETE',
            url=self.url,
            params=self.params,
            headers=headers
        )

        return {
            'data': response.json() if return_representation and response.status_code == 200 else None,
            'status_code': response.status_code
        }


# Example usage functions
def get_all_projects() -> List[Dict[str, Any]]:
    """Get all projects from Supabase"""
    client = SupabaseClient()
    result = client.table('projects').select('*').execute()
    return result['data']


def get_project_by_id(project_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific project by ID"""
    client = SupabaseClient()
    result = client.table('projects').select('*').eq('id', project_id).execute()
    data = result['data']
    return data[0] if data else None


def get_projects_by_country(country: str) -> List[Dict[str, Any]]:
    """Get all projects in a specific country"""
    client = SupabaseClient()
    result = client.table('projects').select('*').eq('country', country).execute()
    return result['data']


def get_projects_by_sector(sector: str) -> List[Dict[str, Any]]:
    """Get all projects in a specific sector"""
    client = SupabaseClient()
    result = client.table('projects').select('*').eq('sector', sector).execute()
    return result['data']


def search_projects(search_term: str) -> List[Dict[str, Any]]:
    """Search projects by name (case-insensitive)"""
    client = SupabaseClient()
    result = client.table('projects').select('*').ilike('name', f'%{search_term}%').execute()
    return result['data']


def create_project(project_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a new project"""
    client = SupabaseClient()
    result = client.table('projects').insert(project_data).execute()
    data = result['data']
    return data[0] if data else None


def update_project(project_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update a project"""
    client = SupabaseClient()
    result = client.table('projects').eq('id', project_id).update(updates).execute()
    data = result['data']
    return data[0] if data else None


def delete_project(project_id: str) -> bool:
    """Delete a project"""
    client = SupabaseClient()
    result = client.table('projects').eq('id', project_id).delete().execute()
    return result['status_code'] in [200, 204]


def get_projects_count() -> int:
    """Get total count of projects"""
    client = SupabaseClient()
    result = client.table('projects').select('id').count('exact').execute()
    return result.get('count', 0)


# CLI usage
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python supabase_config.py <command>")
        print("\nCommands:")
        print("  count          - Get total project count")
        print("  list           - List all projects")
        print("  country <name> - Get projects by country")
        print("  sector <name>  - Get projects by sector")
        print("  search <term>  - Search projects by name")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == 'count':
            count = get_projects_count()
            print(f"Total projects: {count}")

        elif command == 'list':
            projects = get_all_projects()
            print(f"Total projects: {len(projects)}\n")
            for p in projects:
                print(f"  - {p['name']} ({p['country']}) - {p['sector']} [{p['status']}]")

        elif command == 'country' and len(sys.argv) > 2:
            country = sys.argv[2]
            projects = get_projects_by_country(country)
            print(f"Projects in {country}: {len(projects)}\n")
            for p in projects:
                print(f"  - {p['name']} - {p['sector']} [{p['status']}]")

        elif command == 'sector' and len(sys.argv) > 2:
            sector = sys.argv[2]
            projects = get_projects_by_sector(sector)
            print(f"Projects in {sector} sector: {len(projects)}\n")
            for p in projects:
                print(f"  - {p['name']} ({p['country']}) [{p['status']}]")

        elif command == 'search' and len(sys.argv) > 2:
            term = sys.argv[2]
            projects = search_projects(term)
            print(f"Search results for '{term}': {len(projects)}\n")
            for p in projects:
                print(f"  - {p['name']} ({p['country']}) - {p['sector']} [{p['status']}]")

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
