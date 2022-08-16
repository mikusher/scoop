import json
import os
from supersetapiclient.client import SupersetClient

SUPERSET_API_HOST = os.getenv("SUPERSET_API_HOST", "http://localhost:8088/")
SUPERSET_API_USERNAME = os.getenv("SUPERSET_API_USERNAME", "admin")
SUPERSET_API_PASSWORD = os.getenv("SUPERSET_API_PASSWORD", "admin")
DASHBOARD_LOCATION_REPO = os.getenv("DASHBOARD_LOCATION_REPO",
                                    'C:/Users/luist/OfficeDEV/super-docker/superset/docker/dashboards/ASTBusinessKPIsInternalDashboard.json')
DASHBOARD_LOCATION_BK = os.getenv("DASHBOARD_LOCATION_BK",
                                  'C:/Users/luist/OfficeDEV/super-docker/superset/docker/dashboards/ASTBusinessKPIsInternalDashboard_BK.json')


def import_file_dashboard(clt, host, file_path) -> json:
    """Import a file on remote."""
    url = f'{host}/api/v1/dashboard/import'

    file = {
        'formData': (file_path, open(file_path, 'rb'), 'application/json'),
        'overwrite': 'true'
    }

    response = clt.post(url, files=file)
    response.raise_for_status()

    # If import is successful,
    # the following is returned: {'message': 'OK'}
    return response.json()


def update_file_dashboard() -> str:
    client = SupersetClient(host=f'{SUPERSET_API_HOST}', username=f'{SUPERSET_API_USERNAME}',
                            password=f'{SUPERSET_API_PASSWORD}')
    # database
    if client.databases.find(database_name='Analytics-AST').__len__() > 0:
        database_name = client.databases.find(database_name='Analytics-AST')[0]

        # client.databases.add(database_name)
        # print('Analytics-AST database already exists')

        # Get a dashboard by name, if it exists delete it
        if client.dashboards.find(dashboard_title="AST Business KPIs").__len__() > 0:
            dashboard_name = client.dashboards.find(dashboard_title="AST Business KPIs")[0]
            if dashboard_name:
                client.dashboards.export(ids=[dashboard_name.id], path=DASHBOARD_LOCATION_BK)
                print('Backup of AST Business KPIs dashboard created successfully in ' + str(DASHBOARD_LOCATION_BK))
                client.dashboards.delete(dashboard_name.id)
                print('AST Business KPIs dashboard deleted successfully')

        # Import a dashboard
        import_dashboard = import_file_dashboard(clt=client, host=SUPERSET_API_HOST, file_path=DASHBOARD_LOCATION_REPO)
        print('AST Business KPIs dashboard imported successfully')
        dashboard_name = client.dashboards.find(dashboard_title="AST Business KPIs")[0]
        if dashboard_name:
            dashboard_name.published = True
            dashboard_name.slug = "AST-KPI"
            dashboard_name.save()
            print('AST Business KPIs dashboard published successfully ' + str(dashboard_name.id))
            return str(dashboard_name.id)
    else:
        print('Analytics-AST database does not exist')


def evo_container():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    repo_folder = os.path.join(base_dir, '../docker')
    database_yaml = os.path.join(repo_folder, 'database.yaml')
    client = SupersetClient(host=f'{SUPERSET_API_HOST}', username=f'{SUPERSET_API_USERNAME}',
                            password=f'{SUPERSET_API_PASSWORD}')
    # export my database
    for database in client.databases.find():
        if database.database_name == 'Externals':
            client.databases.export(ids=[database.id], path='./database.json')
            print('Backup of Evo database created successfully in ' + str(database_yaml))
            client.databases.delete(database.id)
            print('Evo database deleted successfully')
            break


if __name__ == "__main__":
    evo_container()