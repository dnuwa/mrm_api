
null = None
delete_resource = '''
mutation{
  deleteResource(resourceId:1){
    resource{
      id
      name
      state
      quantity
    }
  }
}
'''

expected_response_after_delete = {
  "data": {
    "deleteResource": {
      "resource": {
        "id": "1",
        "name": "Markers",
        "state": "StateType.archived",
        "quantity": 3
      }
    }
  }
}

delete_non_existent_resource = '''
mutation {
    deleteResource(resourceId: 12) {
        resource {
            id
            name
        }
    }
}
'''
