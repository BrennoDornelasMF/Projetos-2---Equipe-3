from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bibliotecas.models import Biblioteca
from emprestimos.models import Emprestimo
from livros.models import Livro


User = get_user_model()


class DashboardViewTests(TestCase):

	def setUp(self):
		self.admin = User.objects.create_user(
			username='admin',
			password='Teste@12345',
			tipo_usuario='admin',
		)
		self.bibliotecario = User.objects.create_user(
			username='bibliotecario',
			password='Teste@12345',
			tipo_usuario='bibliotecario',
		)
		self.leitor = User.objects.create_user(
			username='leitor',
			password='Teste@12345',
			tipo_usuario='leitor',
		)
		self.biblioteca = Biblioteca.objects.create(
			nome='Biblioteca Central',
			endereco='Rua A, 1',
			cidade='Sao Paulo',
			estado='SP',
			descricao='Biblioteca de testes',
			criado_por=self.bibliotecario,
		)
		self.livro = Livro.objects.create(
			titulo='Livro Base',
			autor='Autor Base',
			categoria='Categoria Base',
			genero='romance',
			descricao='Descricao base',
			quantidade=1,
			disponivel=True,
			status='disponivel',
			biblioteca=self.biblioteca,
		)
		self.emprestimo = Emprestimo.objects.create(
			livro=self.livro,
			leitor=self.leitor,
			biblioteca=self.biblioteca,
			status='pendente',
		)

	def test_dashboard_leitor_mostra_template_de_leitor(self):
		self.client.force_login(self.leitor)

		response = self.client.get(reverse('dashboard'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'dashboard/leitor.html')
		self.assertEqual(response.context['tipo'], 'leitor')

	def test_dashboard_bibliotecario_mostra_template_de_bibliotecario(self):
		self.client.force_login(self.bibliotecario)

		response = self.client.get(reverse('dashboard'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'dashboard/bibliotecario.html')
		self.assertEqual(response.context['tipo'], 'bibliotecario')

	def test_dashboard_admin_mostra_template_de_admin(self):
		self.client.force_login(self.admin)

		response = self.client.get(reverse('dashboard'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'dashboard/admin.html')
		self.assertEqual(response.context['tipo'], 'admin')
