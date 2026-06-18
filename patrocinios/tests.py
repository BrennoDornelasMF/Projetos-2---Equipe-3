from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bibliotecas.models import Biblioteca

from .forms import PatrocinioForm
from .models import Patrocinio


User = get_user_model()


class PatrocinioFormTests(TestCase):

	def test_formulario_e_valido(self):
		form = PatrocinioForm(
			data={
				'nome_patrocinador': 'Empresa X',
				'valor': '1500.00',
				'descricao': 'Apoio cultural',
			}
		)

		self.assertTrue(form.is_valid(), form.errors)


class PatrocinioViewTests(TestCase):

	def setUp(self):
		self.dono = User.objects.create_user(
			username='dono',
			password='Teste@12345',
			tipo_usuario='bibliotecario',
		)
		self.outro = User.objects.create_user(
			username='outro',
			password='Teste@12345',
			tipo_usuario='leitor',
		)
		self.biblioteca = Biblioteca.objects.create(
			nome='Biblioteca Central',
			endereco='Rua A, 1',
			cidade='Sao Paulo',
			estado='SP',
			descricao='Biblioteca de testes',
			criado_por=self.dono,
		)

	def test_registrar_patrocinio_cria_registro_para_dono(self):
		self.client.force_login(self.dono)

		response = self.client.post(
			reverse('registrar_patrocinio', args=[self.biblioteca.id]),
			data={
				'nome_patrocinador': 'Empresa X',
				'valor': '1500.00',
				'descricao': 'Apoio cultural',
			}
		)

		self.assertRedirects(response, reverse('detalhes_biblioteca', args=[self.biblioteca.id]))
		self.assertTrue(Patrocinio.objects.filter(nome_patrocinador='Empresa X').exists())

	def test_registrar_patrocinio_bloqueia_nao_dono(self):
		self.client.force_login(self.outro)

		response = self.client.post(
			reverse('registrar_patrocinio', args=[self.biblioteca.id]),
			data={
				'nome_patrocinador': 'Empresa Bloqueada',
				'valor': '100.00',
				'descricao': 'Nao deve salvar',
			}
		)

		self.assertRedirects(
			response,
			reverse('index'),
			fetch_redirect_response=False,
		)
		self.assertFalse(Patrocinio.objects.filter(nome_patrocinador='Empresa Bloqueada').exists())

	def test_listar_patrocinios_retorna_itens_do_dono(self):
		Patrocinio.objects.create(
			nome_patrocinador='Empresa Y',
			valor=Decimal('200.00'),
			descricao='Apoio',
			biblioteca=self.biblioteca,
		)
		self.client.force_login(self.dono)

		response = self.client.get(reverse('listar_patrocinios', args=[self.biblioteca.id]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Empresa Y')
