from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bibliotecas.models import Biblioteca

from .forms import LivroForm
from .models import Livro


User = get_user_model()


def livro_data(**overrides):
	dados = {
		'titulo': 'Livro Teste',
		'autor': 'Autor Teste',
		'categoria': 'Categoria Teste',
		'genero': 'romance',
		'descricao': 'Descricao do livro teste',
		'quantidade': 2,
		'status': 'disponivel',
	}
	dados.update(overrides)
	return dados


class LivroModelTests(TestCase):

	def setUp(self):
		self.usuario = User.objects.create_user(
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
			criado_por=self.usuario,
		)

	def test_str_retorna_o_titulo(self):
		livro = Livro.objects.create(
			biblioteca=self.biblioteca,
			**livro_data(),
		)

		self.assertEqual(str(livro), 'Livro Teste')


class LivroFormTests(TestCase):

	def test_formulario_e_valido_com_dados_basicos(self):
		form = LivroForm(data=livro_data())

		self.assertTrue(form.is_valid(), form.errors)


class LivroViewTests(TestCase):

	def setUp(self):
		self.bibliotecario = User.objects.create_user(
			username='dono',
			password='Teste@12345',
			tipo_usuario='bibliotecario',
		)
		self.outro_usuario = User.objects.create_user(
			username='outro',
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
		self.livro = Livro.objects.create(
			biblioteca=self.biblioteca,
			**livro_data(titulo='Dom Casmurro', genero='romance', categoria='Clássicos'),
		)

	def test_buscar_livros_filtra_por_texto(self):
		self.client.force_login(self.outro_usuario)

		response = self.client.get(reverse('buscar_livros'), {'busca': 'Dom'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Dom Casmurro')

	def test_buscar_livros_filtra_por_genero(self):
		self.client.force_login(self.outro_usuario)

		response = self.client.get(reverse('buscar_livros'), {'genero': 'romance'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Dom Casmurro')

	def test_adicionar_livro_cria_registro_para_o_dono(self):
		self.client.force_login(self.bibliotecario)

		response = self.client.post(
			reverse('adicionar_livro', args=[self.biblioteca.id]),
			data=livro_data(titulo='Novo Livro', categoria='Ficcao', genero='fantasia')
		)

		self.assertRedirects(response, reverse('detalhes_biblioteca', args=[self.biblioteca.id]))
		self.assertTrue(Livro.objects.filter(titulo='Novo Livro', biblioteca=self.biblioteca).exists())

	def test_adicionar_livro_bloqueia_usuario_nao_dono(self):
		self.client.force_login(self.outro_usuario)

		response = self.client.post(
			reverse('adicionar_livro', args=[self.biblioteca.id]),
			data=livro_data(titulo='Livro Bloqueado')
		)

		self.assertRedirects(
			response,
			reverse('index'),
			fetch_redirect_response=False,
		)
		self.assertFalse(Livro.objects.filter(titulo='Livro Bloqueado').exists())
