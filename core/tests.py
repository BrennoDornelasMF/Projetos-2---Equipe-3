from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class CoreViewTests(TestCase):

	def test_index_exibe_pagina_para_visitante(self):
		response = self.client.get(reverse('index'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'core/index.html')

	def test_index_redireciona_usuario_autenticado(self):
		usuario = User.objects.create_user(
			username='leitor',
			password='Teste@12345',
			tipo_usuario='leitor',
		)
		self.client.force_login(usuario)

		response = self.client.get(reverse('index'))

		self.assertRedirects(response, reverse('dashboard'))
