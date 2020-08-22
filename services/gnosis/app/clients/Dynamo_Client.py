import boto3
from boto3.dynamodb.conditions import Key, Attr
from ..exceptions import Base_Exception


class Dynamo_Client():

    """An interface for AWS DynamoDB client and resource tool with both general
    and resource-specific methods.
    """

    def __init__(self):
        # Set default region
        boto3.setup_default_session(region_name='us-east-1')        
        # Get the service resource.
        self.dynamo_resource = boto3.resource(
            'dynamodb'
        )
        # Get the service client
        self.dynamo_client = boto3.client(
            'dynamodb'
        )
        # Default table for resource-specific methods
        self.userplan_table = self.dynamo_resource.Table('gnosis_user_plans')

    def list_tables(self):
        """General Method -- Lists all DynamoDB tables for current region

        Returns:
            list -- list of DynamoDB table names
        """        
        response = self.dynamo_client.list_tables()
        return response

    def put_item_in_table(self, item, table):
        """General Method -- Inserts item into DynamoDB table

        Arguments:
            item {python dict} -- python dictionary w/ Key, Values to insert
            table {string} -- name of table to be inserted
        """
        # Instantiate table        
        table = self.dynamo_resource.Table(table)
        
        # Insert item
        table.put_item(
            Item=item
        )

    def check_userplan_exists(self, user_id, plan_name):
        """Resource-Specific Method -- Check if user plan to save already exists

        Arguments:
            user_id {string}
            plan_name {string} -- name of user plan to be saved

        Returns:
            boolean -- T/F plan exists
        """ 
        # Check for user plan       
        response = self.userplan_table.get_item(
            Key = {
                'user_id': user_id,
                'plan_name': plan_name
            }
        )
        try:
            response['Item']
            return True
        except KeyError:
            # If no 'Item' userplan name not taken
            return False

    def list_userplan_names(self, user_id):
        """Resource-Specific Method -- List all user's existing plans for
        loading options

        Arguments:
            user_id {string}

        Returns:
            list -- list of user's existing plans. Empty if no plans exist.
        """        
        try:
            # Get list of user's plans
            response = self.userplan_table.query(
                KeyConditionExpression = Key('user_id').eq(user_id)
            )
            items = response['Items']
            userplan_names = []
            # Build list of plan names
            for plan in items:
                userplan_name_json = {
                    'text': plan['plan_name'], 
                    'value': plan['plan_name']
                }
                userplan_names.append(userplan_name_json)
            return userplan_names
        except KeyError:
            # If no 'Items', user has no existing plans.
            return []

    def get_userplan(self, user_id, plan_name):
        """Resource-Specific Method -- Get selected user plan for loading

        Arguments:
            user_id {string}
            plan_name {string} -- name of plan to be loaded

        Raises:
            Base_Exception: plan name is selected from previously queried list 
                so if still no 'Item' it is a backend error.
            
        Returns:
            python list of dicts -- user plan
        """        
        try:
            # Get user plan and graph data
            response = self.userplan_table.get_item(
                Key={
                    'user_id': user_id,
                    'plan_name': plan_name
                }
            )
            userplan = response['Item']
            return userplan
        except KeyError:
            # If backend error
            raise Base_Exception("There was an error on our end.")

