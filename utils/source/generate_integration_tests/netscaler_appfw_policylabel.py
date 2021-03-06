from collections import OrderedDict
import copy
import helpers

from BaseIntegrationModule import BaseIntegrationModule
ENTITY_NAME = 'netscaler_appfw_policylabel'
input_data = OrderedDict()
testbed_data = []

submodObj = BaseIntegrationModule(ENTITY_NAME, 'basic')

attributes = OrderedDict(
    [
        ('state',  'present'),

        ('labelname',  'test_label_name'),
        ('policylabeltype',  'http_req'),

    ]
)

submodObj.add_operation('setup', copy.deepcopy(attributes))

# Verify existing values
verification_dict = copy.deepcopy(attributes)
del verification_dict['state']
verification_dict['labelname'] = '"%s"' % verification_dict['labelname']
verification_dict['policylabeltype'] = '"%s"' % verification_dict['policylabeltype']

data = helpers.get_verification_playbook_dict(
    nitro_resource='appfwpolicylabel',
    nitro_resource_name='test_label_name',
    verification_dict=verification_dict,
)
submodObj.add_raw_operation('verify', data, run_once=True)

attributes['state'] = 'absent'

submodObj.add_operation('remove', copy.deepcopy(attributes))



input_data.update({submodObj.get_sub_mod_name(): copy.deepcopy(submodObj.get_mod_attrib())})
