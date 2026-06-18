from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bibliotecas.models import Biblioteca
from livros.models import Livro

from .models import (
	AvisoDisponibilidade,
	Desafio,
	Doacao,
	Emprestimo,
	ParticipacaoDesafio,
	Sugestao,
	VotoSugestao,
)


User = get_user_model()


def livro_base(biblioteca, **overrides):
	dados = {
		'titulo': 'Livro Base',
		'autor': 'Autor Base',
		'categoria': 'Categoria Base',
		'genero': 'romance',
		'descricao': 'Descricao base',
		'quantidade': 2,
		'disponivel': True,
		'status': 'disponivel',
		'biblioteca': biblioteca,
	}
	dados.update(overrides)
	return Livro.objects.create(**dados)


class EmprestimoModelTests(TestCase):

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
		self.livro = livro_base(self.biblioteca)

	def test_dias_restantes_e_atraso(self):
		emprestimo = Emprestimo.objects.create(
			livro=self.livro,
			leitor=self.leitor,
			biblioteca=self.biblioteca,
			status='emprestado',
			data_devolucao=timezone.now().date() + timedelta(days=5),
		)

		self.assertEqual(emprestimo.dias_restantes(), 5)
		self.assertEqual(emprestimo.dias_atraso(), 0)

	def test_dias_atraso_para_data_passada(self):
		emprestimo = Emprestimo.objects.create(
			livro=self.livro,
			leitor=self.leitor,
			biblioteca=self.biblioteca,
			status='emprestado',
			data_devolucao=timezone.now().date() - timedelta(days=3),
		)

		self.assertEqual(emprestimo.dias_restantes(), -3)
		self.assertEqual(emprestimo.dias_atraso(), 3)


class DoacaoViewTests(TestCase):

	def setUp(self):
		self.bibliotecario = User.objects.create_user(
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
			criado_por=self.bibliotecario,
		)
		self.livro = livro_base(self.biblioteca, titulo='Livro Existente', quantidade=1)

	def test_registrar_doacao_incrementa_quantidade_do_livro_existente(self):
		self.client.force_login(self.bibliotecario)

		response = self.client.post(
			reverse('registrar_doacao', args=[self.biblioteca.id]),
			data={
				'titulo': 'Livro Existente',
				'autor': 'Autor Base',
				'categoria': 'Categoria Base',
				'descricao': 'Doacao de teste',
				'quantidade': 2,
				'nome_doador': 'Doador Teste',
			}
		)

		self.assertRedirects(response, reverse('detalhes_biblioteca', args=[self.biblioteca.id]))
		self.livro.refresh_from_db()
		self.assertEqual(self.livro.quantidade, 3)
		self.assertTrue(Doacao.objects.filter(nome_doador='Doador Teste').exists())

	def test_registrar_doacao_bloqueia_nao_dono(self):
		self.client.force_login(self.outro)

		response = self.client.post(
			reverse('registrar_doacao', args=[self.biblioteca.id]),
			data={
				'titulo': 'Livro Novo',
				'autor': 'Autor Base',
				'categoria': 'Categoria Base',
				'descricao': 'Doacao bloqueada',
				'quantidade': 1,
				'nome_doador': 'Doador Bloqueado',
			}
		)

		self.assertRedirects(
			response,
			reverse('index'),
			fetch_redirect_response=False,
		)
		self.assertFalse(Doacao.objects.filter(nome_doador='Doador Bloqueado').exists())


class SugestaoViewTests(TestCase):

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
		self.livro = livro_base(self.biblioteca)

	def test_sugerir_titulo_cria_sugestao_para_leitor(self):
		self.client.force_login(self.leitor)

		response = self.client.post(
			reverse('sugerir_titulo'),
			data={
				'titulo': 'Novo Livro',
				'autor': 'Autor Novo',
				'descricao': 'Descricao',
				'biblioteca': self.biblioteca.id,
			}
		)

		self.assertRedirects(response, reverse('listar_sugestoes'))
		sugestao = Sugestao.objects.get(titulo='Novo Livro')
		self.assertEqual(sugestao.leitor, self.leitor)
		self.assertEqual(sugestao.biblioteca, self.biblioteca)

	def test_votar_sugestao_incrementa_votos_once(self):
		sugestao = Sugestao.objects.create(
			titulo='Sugestao Teste',
			autor='Autor Teste',
			descricao='Descricao',
			biblioteca=self.biblioteca,
			leitor=self.leitor,
		)
		self.client.force_login(self.leitor)

		response = self.client.get(reverse('votar_sugestao', args=[sugestao.id]))

		self.assertRedirects(response, reverse('listar_sugestoes'))
		sugestao.refresh_from_db()
		self.assertEqual(sugestao.votos, 1)
		self.assertTrue(VotoSugestao.objects.filter(sugestao=sugestao, leitor=self.leitor).exists())


class DesafioModelTests(TestCase):

	def setUp(self):
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

	def test_esta_ativo_depende_da_data_final(self):
		desafio = Desafio.objects.create(
			titulo='Desafio Ativo',
			descricao='Descricao',
			biblioteca=self.biblioteca,
			meta=5,
			data_fim=timezone.now().date() + timedelta(days=2),
		)

		self.assertTrue(desafio.esta_ativo())

	def test_progresso_percentual_limita_em_100(self):
		desafio = Desafio.objects.create(
			titulo='Desafio Progresso',
			descricao='Descricao',
			biblioteca=self.biblioteca,
			meta=4,
			data_fim=timezone.now().date() + timedelta(days=2),
		)
		participacao = ParticipacaoDesafio.objects.create(
			desafio=desafio,
			leitor=self.leitor,
			livros_lidos=6,
		)

		self.assertEqual(participacao.progresso_percentual(), 100)
