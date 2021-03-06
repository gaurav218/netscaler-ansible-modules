from collections import OrderedDict

class BaseIntegrationModule(object):
    """docstring for SubModule"""
    def __init__(self, entity_name, sub_mod_name=''):
        self.entity_name = entity_name 
        self.sub_mod_name = entity_name if not sub_mod_name else sub_mod_name
        self.submodule_attrib = [] # OrderedDict() 
        self.testbed_attrib = []

    def get_sub_mod_name(self):
        return self.sub_mod_name

    def get_mod_attrib(self):
        return self.submodule_attrib

    def get_testbed_attrib(self):
        return self.testbed_attrib

    def add_common_attributes(self, op_name, op_dict, is_testbed=False):
        op_dict['name'] = '{} {}'.format(op_name.upper(), self.sub_mod_name)
        op_dict['delegate_to'] = 'localhost' 
        if not is_testbed:
            op_dict['register'] = 'result' 
            op_dict['check_mode'] = '{{ check_mode }}' 
        #op_dict['VERIFY_CHECK_MODE'] = True
        #op_dict['VERIFY_IDEMPOTENCY'] = True 

        op_dict[self.entity_name] = OrderedDict()
        op_dict[self.entity_name]['nitro_user'] = "{{ nitro_user }}"
        op_dict[self.entity_name]['nitro_pass'] = "{{ nitro_pass }}"
        op_dict[self.entity_name]['nsip'] = "{{ nsip }}"
        op_dict[self.entity_name]['nsip'] = "{{ nsip }}"

    def add_testbed(self, testbed_name, testbed_data):
        testbed_dict = OrderedDict()
        testbed_name = "{}__{}".format('testbed',testbed_name)
        self.add_common_attributes(testbed_name, testbed_dict, is_testbed=True)
        testbed_dict[self.entity_name]['state'] = "{{ state }}"

        # if testbed_data is list, it means the order of 2nd element has to be maintained
        if type(testbed_data) == list:
            for key in testbed_data[0].keys():
                testbed_dict[self.entity_name][key] = testbed_data[0][key]

            for key in testbed_data[1].keys():
                testbed_dict[key] = testbed_data[1][key]
 
        else:
            for key in testbed_data.keys():
                testbed_dict[self.entity_name][key] = testbed_data[key]
        
        return testbed_dict

    def add_operation(self, op_name, op_data, run_once=False):
        task_list = []
        # if op_data is list, it means it has more than one task in the same operation
        if type(op_data) == list:
            for task in op_data:
                op_dict = OrderedDict()
                self.add_common_attributes(op_name, op_dict)
                if type(task) == list: # the second item is extra_vars (it is usually with_sequence
                    for key in task[0].keys():
                        op_dict[self.entity_name][key] = task[0][key]

                    for key in task[1].keys():
                        op_dict[key] = task[1][key]

                else:
                    for key in task.keys():
                        op_dict[self.entity_name][key] = task[key]
                task_list.append(op_dict)
        else:
            op_dict = OrderedDict()
            self.add_common_attributes(op_name, op_dict)
    
            for key in op_data.keys():
                op_dict[self.entity_name][key] = op_data[key]
            task_list.append(op_dict)
    
        self.submodule_attrib.append({op_name: task_list, 'run_once':run_once})

    def add_raw_operation(self, op_name, op_data, run_once=False):
        self.submodule_attrib.append({op_name: op_data, 'run_once':run_once})
