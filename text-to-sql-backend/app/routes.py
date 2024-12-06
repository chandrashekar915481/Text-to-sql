from flask import Blueprint, request, jsonify, current_app
from app.database import Database
from app.utils import SQLGenerator, validate_sql
from app.models import SQLRequest, SQLResponse

main = Blueprint('main', __name__)

# Initialize SQL Generator as None
_sql_generator = None

def get_sql_generator():
    """Lazy initialization of SQL generator"""
    global _sql_generator
    if _sql_generator is None:
        _sql_generator = SQLGenerator(current_app.config['MODEL_PATH'])
    return _sql_generator

import logging

def execute_schema(db, context):
    """
    Execute the schema creation and insert statements with drop-and-recreate logic.
    """
    import logging

    try:
        # Split the context into individual SQL statements
        statements = [stmt.strip() for stmt in context.split(';') if stmt.strip()]
        
        for statement in statements:
            print("into for")
            if 'CREATE TABLE' in statement.upper():
                print("into if")
                statement_parts = statement.split(' ', 3)
                print(statement_parts)
                print(statement_parts[0].upper())
                print(statement_parts[1].upper())
                if len(statement_parts) > 2 and statement_parts[0].upper() == 'CREATE' and statement_parts[1].upper() == 'TABLE':
                    table_name = statement_parts[2]
                    
                    # Drop the table if it already exists
                    print("drop")
                    drop_statement = f"DROP TABLE IF EXISTS {table_name};"
                    logging.info(f"Dropping table if exists: {table_name}")
                    db.execute_query(drop_statement)
                    
                    # Recreate the table
                    statement = f"{statement_parts[0]} {statement_parts[1]} {table_name} {statement_parts[3]}"
            
            # Log and execute the statement
            logging.info(f"Executing SQL: {statement}")
            db.execute_query(statement)

        return None  # No errors
    except Exception as e:
        logging.error(f"Schema execution error: {e}")
        return str(e)



@main.route('/api/generate-and-execute', methods=['POST'])
def generate_and_execute():
    try:
        data = request.get_json()
        context = data.get('context', '')
        prompt = data.get('prompt', '')
        
        # Get or initialize SQL generator
        generator = get_sql_generator()
        # Create database connection
        db = Database(current_app.config['DATABASE_PATH'])
        
        # First, execute the schema creation
        schema_error = execute_schema(db, context)
        if schema_error:
            return jsonify({
                "generated_sql": "",
                "results": [],
                "error": f"Schema creation error: {schema_error}"
            }), 400
        
        # Generate SQL
        generated_sql = generator.generate_sql(context, prompt)
        print(generated_sql)
        # Execute the generated query
        try:
            results = db.execute_query(generated_sql)
            return jsonify({
                "generated_sql": generated_sql,
                "results": results
            })
        except Exception as e:
            return jsonify({
                "generated_sql": generated_sql,
                "results": [],
                "error": str(e)
            }), 400
            
    except Exception as e:
        return jsonify({
            "generated_sql": "",
            "results": [],
            "error": str(e)
        }), 500