import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from task.models import Task

User = get_user_model()


class ViewsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.domain = 'http://127.0.0.1:8000/api/v1'
        cls.tasks_url = f'{cls.domain}/tasks/'
        cls.task_history_url = f'{cls.domain}/task-history/'
        cls.user_1 = User.objects.create(
            username='username'
        )
        cls.task_1 = Task.objects.create(
            author=cls.user_1,
            title='Название первой задачи',
            description='Описание первой задачи',
            finished='2022-09-13',
            status='new'
        )
        cls.user_2 = User.objects.create(
            username='username_2'
        )
        cls.task_2 = Task.objects.create(
            author=cls.user_2,
            title='Название первой задачи 2-го юзера',
            description='Описание первой задачи 2-го юзера',
            finished='2022-09-13',
            status='new'
        )

    def setUp(self):
        token_1 = Token.objects.create(user=self.user_1)
        self.authorized_client = APIClient()
        self.authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Token {token_1.key}'
        )

    def test_get_tasks_list_retrieve_filtering(self):
        """Проверяет получение списка своих задач, одной задачи, а также
        фильтрацию задач по статусу и планируемому времени завершения"""
        subtests_tuple = (
            (self.tasks_url, 'get tasks list'),
            (f'{self.tasks_url}{self.task_1.id}/', 'get task'),
            (
                f'{self.tasks_url}?status={self.task_1.status}',
                'filtering by status'
            ),
            (
                f'{self.tasks_url}?finished={self.task_1.finished}',
                'filtering by planned completion time'
            ),
            (
                f'{self.tasks_url}?finished={self.task_1.finished}&status={self.task_1.status}',
                'filtering by planned completion time and status'
            ),
        )
        for address, subtest_description in subtests_tuple:
            with self.subTest(subtest_description):
                response = self.authorized_client.get(path=address)
                json = response.json()
                if type(json) == list:
                    task = json[0]
                else:
                    task = json
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(task['id'], self.task_1.id)
                self.assertEqual(task['author'], self.task_1.author.username)
                self.assertEqual(task['title'], self.task_1.title)
                self.assertEqual(task['description'], self.task_1.description)
                self.assertTrue('created' in task)
                self.assertEqual(task['status'], self.task_1.status)
                self.assertEqual(
                    task['finished'],
                    self.task_1.finished
                )

    def test_post_task(self):
        """Проверяет создание задачи"""
        task_count = Task.objects.count()
        post_data = {
            'title': 'Название второй задачи',
            'description': 'Описание второй задачи',
            'finished': '2022-10-01',
            'status': 'planned'
        }
        response = self.authorized_client.post(
            path=self.tasks_url,
            data=post_data,
        )
        task = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), task_count + 1)
        self.assertTrue(
            Task.objects.filter(id=task['id']).exists()
        )
        self.assertEqual(task['author'], self.user_1.username)
        self.assertEqual(task['title'], post_data['title'])
        self.assertEqual(task['description'], post_data['description'])
        self.assertTrue('created' in task)
        self.assertEqual(task['status'], post_data['status'])
        self.assertEqual(
            task['finished'],
            post_data['finished']
        )

    def test_put_task(self):
        """Проверяет замену задачи"""
        put_data = {
            'title': 'Название замененной задачи',
            'description': 'Описание замененной задачи',
            'finished': '2022-11-05',
            'status': 'in_progress'
        }
        response = self.authorized_client.put(
            path=f'{self.tasks_url}{self.task_1.id}/',
            data=put_data,
        )
        task = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task['id'], self.task_1.id)
        self.assertEqual(task['author'], self.task_1.author.username)
        self.assertEqual(task['title'], put_data['title'])
        self.assertEqual(task['description'], put_data['description'])
        self.assertEqual(
            task['created'],
            datetime.datetime.isoformat(self.task_1.created)
        )
        self.assertEqual(task['status'], put_data['status'])
        self.assertEqual(
            task['finished'],
            put_data['finished']
        )

    def test_patch_task(self):
        """Проверяет изменение задачи"""
        patch_data = {
            'title': 'Название измененной задачи',
            'status': 'completed'
        }
        response = self.authorized_client.patch(
            path=f'{self.tasks_url}{self.task_1.id}/',
            data=patch_data,
        )
        task = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task['id'], self.task_1.id)
        self.assertEqual(task['author'], self.task_1.author.username)
        self.assertEqual(task['title'], patch_data['title'])
        self.assertEqual(task['description'], self.task_1.description)
        self.assertEqual(
            task['created'],
            datetime.datetime.isoformat(self.task_1.created)
        )
        self.assertEqual(task['status'], patch_data['status'])
        self.assertEqual(
            task['finished'],
            self.task_1.finished
        )

    def test_delete_task(self):
        """Проверяет удаление задачи"""
        response = self.authorized_client.delete(
            path=f'{self.tasks_url}{self.task_1.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Task.objects.filter(id=self.task_1.id).exists()
        )

    def test_get_task_history(self):
        """Проверяет получение истории изменения задачи"""
        change_data = {'title': 'Название измененной задачи'}
        self.authorized_client.patch(
            path=f'{self.tasks_url}{self.task_1.id}/',
            data=change_data,
        )
        response = self.authorized_client.get(
            path=f'{self.task_history_url}{self.task_1.id}/'
        )
        task = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task_1.history.count(), 2)
        self.assertEqual(task['history'][0]['title'], change_data['title'])
        self.assertEqual(task['history'][0]['description'], None)
        self.assertEqual(task['history'][0]['status'], None)
        self.assertEqual(task['history'][0]['finished'], None)
        self.assertTrue('date_change' in task['history'][0])
        self.assertEqual(task['history'][1]['title'], self.task_1.title)
        self.assertEqual(
            task['history'][1]['description'],
            self.task_1.description
        )
        self.assertEqual(task['history'][1]['status'], self.task_1.status)
        self.assertEqual(
            task['history'][1]['finished'],
            self.task_1.finished
        )

    def test_not_view_other_user_tasks(self):
        """Проверяет, что пользователь не может просматривать чужие задачи"""
        response = self.authorized_client.get(
            path=f'{self.tasks_url}{self.task_2.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
