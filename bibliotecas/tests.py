from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import BibliotecaForm
from .models import Biblioteca


User = get_user_model()


def biblioteca_data(**overrides):
	dados = {
		'nome': 'Biblioteca Teste',
		'endereco': 'Rua Principal, 100',
		'cidade': 'Sao Paulo',
		'estado': 'SP',
		'descricao': 'Descricao de teste',
	}
	dados.update(overrides)
	return dados


class BibliotecaFormTests(TestCase):

	def test_formulario_e_valido(self):
		form = BibliotecaForm(data=biblioteca_data())

		self.assertTrue(form.is_valid(), form.errors)


class BibliotecaViewTests(TestCase):

	def setUp(self):
		self.leitor = User.objects.create_user(
			username='leitor',
			password='Teste@12345',
			tipo_usuario='leitor',
		)
		self.bibliotecario = User.objects.create_user(
			username='bibliotecario',
			password='Teste@12345',
			tipo_usuario='bibliotecario',
		)
		self.biblioteca = Biblioteca.objects.create(
			nome='Biblioteca Central',
			endereco='Rua A, 1',
			cidade='Sao Paulo',
			estado='SP',
			descricao='Biblioteca de testes',
			criado_por=self.bibliotecario,
		)

	def test_bibliotecas_leitor_exige_usuario_leitor(self):
		self.client.force_login(self.bibliotecario)

		response = self.client.get(reverse('bibliotecas_leitor'))

		self.assertRedirects(
			response,
			reverse('index'),
			fetch_redirect_response=False,
		)

	def test_bibliotecas_leitor_permite_usuario_leitor(self):
		self.client.force_login(self.leitor)

		response = self.client.get(reverse('bibliotecas_leitor'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Biblioteca Central')

	def test_detalhes_biblioteca_exibe_dados(self):
		self.client.force_login(self.leitor)

		response = self.client.get(reverse('detalhes_biblioteca', args=[self.biblioteca.id]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Biblioteca Central')

	def test_painel_bibliotecario_bloqueia_leitor(self):
		self.client.force_login(self.leitor)

		response = self.client.get(reverse('painel_bibliotecario'))

		self.assertRedirects(
			response,
			reverse('index'),
			fetch_redirect_response=False,
		)
