# Parent class for module controller classes
from .config import API_URL, basic_auth
from .restapi import Client


class CWController(Client):
    def __init__(self, url=None, auth=None):
        # self.module_url comes from child
        # self.module comes from child
        # self._class comes from child
        self.conditions = ''
        self.orderBy = ''
        self.childconditions = ''
        self.customfieldconditions = ''
        self.page = ''
        self.pageSize = ''
        self.API_URL = url if url is not None else API_URL
        self.basic_auth = auth if auth is not None else basic_auth
        super().__init__('{}/{}'.format(self.API_URL, self.module_url))

    def _format_user_params(self):
        user_params = {}
        for param in ['conditions', 'orderBy', 'childconditions', 'customfieldconditions', 'page', 'pageSize', 'recordId', 'recordType']:
            if getattr(self, param) != '':
              user_params[param] = getattr(self, param)
        return user_params

    def _get(self):
        json_results = getattr(self, self.module).get(user_headers=self.basic_auth,
                                                      user_params=self._format_user_params())
        for json in json_results:
            yield self._class(json)

    def _create(self, a_object):
        # Ideally take the_item and submit that as the user_data
        try:
            clean_dict = {k: v for k, v in a_object.__dict__.items() if v}
        except Exception as e:
            print(repr(e))
            return False
        an_instance = self._class(
            getattr(self, self.module).post(user_data=clean_dict, user_headers=self.basic_auth))
        return an_instance
    
    def _upload(self, objectType, objectId, title, filename, f):
        multipart_form_data = {
              'recordType': (None, objectType),
              'recordId': (None, objectId),
              'Title': (None, title),
              'file': (filename, f)
          }
        an_instance = self._class(
              getattr(self, self.module).post([], files=multipart_form_data, user_headers=self.basic_auth))
        return an_instance

    def _get_count(self):
        json_results = getattr(self, self.module).get(the_id='count', user_headers=self.basic_auth,
                                                      user_params=self._format_user_params())
        count = json_results['count']
        return count

    def _get_by_id(self, item_id):
        an_instance = self._class(getattr(self, self.module).get(the_id=item_id, user_headers=self.basic_auth))
        return an_instance

    def _delete_by_id(self, item_id):
        return getattr(self, self.module).delete(the_id=item_id, user_headers=self.basic_auth)

    def _replace(self, item_id):  # TODO: test
        an_instance = self._class(
            getattr(self, self.module).put(the_id=item_id, user_data=self.clean_dict, user_headers=self.basic_auth))
        return an_instance

    def _update(self, item_id, key, value):
        # build PatchOperation dict
        patch_operation = [{
            'op': 'replace',
            'path': key,
            'value': value
        }]
        # call Patch method on API
        an_instance = self._class(getattr(self, self.module).patch(the_id=item_id, user_data=patch_operation,
                                                                   user_headers=self.basic_auth))
        return an_instance

    def _update_multiple_keys(self, item_id, keys_dict):
        # build PatchOperation dict
        patch_operation = []
        for key, value in keys_dict.items():
            patch_dict = {'op': 'replace', 'path': key, 'value': value}
            patch_operation.append(patch_dict)

        # call Patch method on API
        an_instance = self._class(getattr(self, self.module).patch(the_id=item_id, user_data=patch_operation,
                                                                   user_headers=self.basic_auth))
        return an_instance



    def _merge(self, a_object, target_id):  # TODO: test
        # try:
        #     clean_dict = {k: v for k, v in a_object.__dict__.items() if v}
        # except Exception as e:
        #     print(repr(e))
        #     return False
        # clean_dict['toCompanyId'] = target_id
        # response = getattr(self, self.module).post(user_data=clean_dict, the_id='/'.join([str(a_object.id), 'merge']),
        #                                            user_headers=self.basic_auth)
        # return response
        pass

    def _post_dict(self, item_id, the_dict):  # TODO: test
        # Ideally take the_item and submit that as the user_data
        try:
            clean_dict = {k: v for k, v in the_dict.items() if v}
        except Exception as e:
            print(repr(e))
            return False
        an_instance = self._class(
            getattr(self, self.module).post(the_id=item_id, user_data=clean_dict, user_headers=self.basic_auth))
        return an_instance

