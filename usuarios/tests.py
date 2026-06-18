from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CadastroForm


User = get_user_model()


def cadastro_data(
	username='novo_usuario',
	password='Teste@12345',
	tipo_usuario='leitor',
):
	return {
		'username': username,
		'email': f'{username}@example.com',
		'tipo_usuario': tipo_usuario,
		'nome_completo': 'Usuario Teste',
		'cpf': '123.456.789-10',
		'telefone': '(11) 99999-9999',
		'data_nascimento': '2000-01-01',
		'cep': '00000-000',
		'rua': 'Rua Teste',
		'numero': '100',
		'bairro': 'Centro',
		'cidade': 'Sao Paulo',
		'estado': 'SP',
		'password1': password,
		'password2': password,
	}


class CadastroFormTests(TestCase):

	def test_formulario_valido_cria_usuario(self):
		form = CadastroForm(data=cadastro_data())

		self.assertTrue(form.is_valid(), form.errors)

		usuario = form.save()

		self.assertEqual(usuario.username, 'novo_usuario')
		self.assertTrue(usuario.check_password('Teste@12345'))
		self.assertEqual(usuario.tipo_usuario, 'leitor')

	def test_formulario_rejeita_senhas_diferentes(self):
		dados = cadastro_data()
		dados['password2'] = 'Outra@12345'

		form = CadastroForm(data=dados)

		self.assertFalse(form.is_valid())
		self.assertIn('password2', form.errors)


class UsuarioViewTests(TestCase):

	def test_cadastro_view_cria_usuario(self):
		response = self.client.post(reverse('cadastro'), data=cadastro_data('cadastro_view'))

		self.assertRedirects(response, reverse('login'))
		self.assertTrue(User.objects.filter(username='cadastro_view').exists())

	def test_cadastro_view_exibe_erros_quando_senhas_diferem(self):
		dados = cadastro_data('cadastro_invalido')
		dados['password2'] = 'SenhaDiferente@123'

		response = self.client.post(reverse('cadastro'), data=dados)

		self.assertEqual(response.status_code, 200)
		self.assertIn('password2', response.context['form'].errors)
		self.assertFalse(User.objects.filter(username='cadastro_invalido').exists())

	def test_login_view_redireciona_leitor_para_bibliotecas(self):
		User.objects.create_user(
			username='leitor',
			email='leitor@example.com',
			password='Teste@12345',
			tipo_usuario='leitor',
		)

		response = self.client.post(
			reverse('login'),
			{'username': 'leitor', 'password': 'Teste@12345'}
		)

		self.assertRedirects(response, reverse('bibliotecas_leitor'))

	def test_login_view_redireciona_bibliotecario_para_painel(self):
		User.objects.create_user(
			username='bibliotecario',
			email='bibliotecario@example.com',
			password='Teste@12345',
			tipo_usuario='bibliotecario',
		)

		response = self.client.post(
			reverse('login'),
			{'username': 'bibliotecario', 'password': 'Teste@12345'}
		)

		self.assertRedirects(response, reverse('painel_bibliotecario'))

	def test_login_view_redireciona_admin_para_dashboard(self):
		User.objects.create_user(
			username='admin_teste',
			email='admin@example.com',
			password='Teste@12345',
			tipo_usuario='admin',
		)

		response = self.client.post(
			reverse('login'),
			{'username': 'admin_teste', 'password': 'Teste@12345'}
		)

		self.assertRedirects(response, reverse('dashboard'))

	def test_logout_view_redireciona_para_index(self):
		usuario = User.objects.create_user(
			username='logout_user',
			email='logout@example.com',
			password='Teste@12345',
			tipo_usuario='leitor',
		)
		self.client.force_login(usuario)

		response = self.client.get(reverse('logout'))

		self.assertRedirects(response, reverse('index'))
