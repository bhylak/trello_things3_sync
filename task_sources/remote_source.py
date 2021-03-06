from tasks.remote_task import RemoteTask
import pytz

class RemoteSource(object):


    def __init__(self):
        '''todo'''
        self._cache = {}
        self._newly_added = []
        self._newly_removed = []
        self._seen_ids = []
        self.list_sources = {}

        if not hasattr(self, "names_to_status"):
            self.names_to_status = {}
            Exception("No names to status map found. Remote source will not function properly")

        self.status_to_names = {v: k for k, v in self.names_to_status.iteritems()}  # create reverse of map for lookup

    # def add_new(self, task): #todo add function for adding to remote
    # new_card = RemoteTask("", self)

    def get_newly_added(self):
        return self._newly_added

    def convert_date_for_py(self, date):
        if date is not None:
            try:
                date = pytz.utc.localize(date)
            except:
                pass

        return date

    def _init_update_(self):

        self._newly_added = []
        self._newly_removed = []
        self._seen_ids = []

        print "Started to update lists... Cache size: " + str(len(self._cache))

        '''Rest of function must be implemented'''

    def get_all_tasks(self):
        '''std remote source func'''
        '''returns all cards across all lists'''
        return self._cache

    def update_task(self, remote_task, fetch=False):
        # abstract func. must be implemented
        print ''

    def add_task(self, task):
        # abstract func. must be implemented
        print ''

    def process_task(self, remote_task):
        self._seen_ids.append(remote_task.id)
        self.update_task(remote_task)

    def _post_update_(self):

        to_delete = []

        for item_id in self._cache:
            if item_id not in self._seen_ids:  # not seen in last update, so must be stale
                to_delete.append(item_id)

        for item_id in to_delete:
            del self._cache[item_id]
            print "Deleted " + str(item_id)

        for task in self._cache.values():
            self.process_task(task)

    def list_to_state(self, list_name):
        return self.status_to_names.get(list_name, None)

    def get_list(self, name):
        return self.list_sources[name]

    def state_to_list(self, state):  # todo need a list state, so inverse of this
        return self.status_to_names.get(state, None)

    def push_changes(self, task):
        '''to implement'''

    def add_to_cache(self, item_id, data):

        remote_task = RemoteTask(item_id, data, self)
        self._cache[item_id] = remote_task

        return remote_task

