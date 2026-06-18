from django.test import TestCase


class ForumSmokeTests(TestCase):

	def test_modulos_forum_importam(self):
		from forum import models, views

		self.assertTrue(hasattr(models, '__name__'))
		self.assertTrue(hasattr(views, '__name__'))
