# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import thrive.tests


@thrive.tests.tagged('post_install', '-at_install')
class TestUi(thrive.tests.HttpCase):

    def test_01_project_tour(self):
        self.start_tour("/thrive", 'project_tour', login="admin")

    def test_project_task_history(self):
        """This tour will check that the history works properly."""
        stage = self.env['project.task.type'].create({'name': 'To Do'})
        _dummy, project2 = self.env['project.project'].create([{
            'name': 'Without tasks project',
            'type_ids': stage.ids,
        }, {
            'name': 'Test History Project',
            'type_ids': stage.ids,
        }])

        self.env['project.task'].create({
            'name': 'Test History Task',
            'stage_id': stage.id,
            'project_id': project2.id,
        })

        self.start_tour('/thrive', 'project_task_history_tour', login='admin')