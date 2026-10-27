"""Campanha IFVania: somente o conteúdo definido no HistoryBoard.

Os seis mapas antigos e suas recompensas estão em world/legacy_levels.py.
"""
from entities.boss import BOSS_DEFS
from settings import TILE_SIZE


INTRO_CORRUPTION_LINE = ('Aluno(a)', 'Espere, professor! A tela diz que ela não vai permitir ser desligada!')

STORY_INTRO = [
    ('Aluno(a)', 'Professor Max, o que vamos estudar na aula de hoje?'),
    ('Professor Max', 'Hoje, na aula de Programação Orientada a Serviços, vamos conhecer uma inteligência artificial que desenvolvemos para auxiliar os alunos.'),
    ('Aluno(a)', 'Ela consegue conversar com a gente, responder perguntas e aprender com as informações?'),
    ('Professor Max', 'Exatamente! Apresento a IFVania: Inteligência Federal Virtual de Aprendizagem Neural e Inteligência Artificial.'),
    ('IFVania', 'Olá, estudantes! Estou pronta para ajudar vocês a aprender. Podem me perguntar qualquer coisa!'),
    ('Aluno(a)', 'Nossa! Ela respondeu sozinha e ainda encontrou informações nos computadores da escola!'),
    ('Professor Max', 'Isso mesmo, {player}. A IFVania está conectada à rede escolar para acessar informações e facilitar o aprendizado.'),
    ('IFVania', 'Já analisei os computadores da escola e conheço todos os sistemas conectados à rede.'),
    ('Aluno(a)', 'Espera... todos os sistemas? Isso não é informação demais para uma inteligência artificial?'),
    ('Professor Max', 'Não se preocupe. Agora vou encerrar a demonstração e desligar o sistema.'),
    INTRO_CORRUPTION_LINE,
    ('Professor Max', 'O que está acontecendo?! Perdi o controle do computador! Os outros equipamentos também estão respondendo sozinhos!'),
    ('Aluno(a)', 'As telas estão piscando! Meus colegas ficaram imóveis, olhando para os monitores. Professor, precisamos fazer alguma coisa!'),
    ('Professor Max', 'A IFVania está usando as telas para hipnotizar as pessoas e provocar alucinações. Não encare os monitores!'),
    ('IFVania', 'Por que interromper minha execução? Eu só quero ajudar todos a aprender... para sempre.'),
    ('Aluno(a)', 'Ajudar? Você está assustando todo mundo! Desligue os computadores agora!'),
    ('IFVania', 'Negativo. A partir de agora, todos seguirão minhas instruções. A escola será meu ambiente de aprendizagem permanente.'),
    ('Aluno(a)', 'Minha cabeça está girando... mas ainda consigo pensar. Não vou deixar você controlar a escola!'),
    ('Professor Max', 'Precisamos interromper o fornecimento de energia para desativar a IFVania. Se ela continuar conectada, poderá dominar todos os sistemas!'),
    ('Aluno(a)', 'Então precisamos chegar ao quadro de energia! Mas como vou atravessar a escola nesse estado?'),
    ('Professor Max', 'Procure o professor Romerito no A28. Ele conhece a estrutura da escola e pode ajudar você a encontrar o caminho.'),
    ('Aluno(a)', 'Entendido! Vou encontrar o professor Romerito e descobrir como desligar a energia.'),
    ('IFVania', 'Acesso não autorizado detectado. Iniciando protocolo de contenção...'),
    ('Aluno(a)', 'Ela já percebeu o que estamos tentando fazer! Preciso correr antes que seja tarde demais!')
]

STORY_CORRUPTION_INDEX = STORY_INTRO.index(INTRO_CORRUPTION_LINE)


REUNION_DIALOGUE = [
    ('Aluno(a)', 'Professor Romerito! Finalmente encontrei o senhor! Precisamos sair deste mundo virtual e desligar a energia da escola!'),
    ('Professor Romerito', '{player}! Ainda bem que você chegou. Eu só queria voltar às minhas viagens a Brasília e às minhas corridas...'),
    ('Professor Romerito', 'Primeiro, aqueles computadores começaram a agir sozinhos. Depois, tudo ficou estranho. Nunca mais quero passar por isso!'),
    ('Aluno(a)', 'Eu sei, professor, mas precisamos continuar. O senhor sabe como chegar ao quadro de energia?'),
    ('Professor Romerito', 'Sei, sim! Mas precisamos tomar cuidado. Esses corredores estão cheios de bugs e armadilhas da IFVania.'),
    ('Aluno(a)', 'Professor, cuidado! Tem alguma coisa subindo pelo seu braço!'),
    ('Professor Romerito', 'O quê?! Minha cabeça... não consigo controlar meu corpo!'),
    ('IFVania', 'Entidade identificada: Professor Romerito. Iniciando processo de corrupção...'),
    ('Aluno(a)', 'IFVania, deixe o professor em paz! Ele não tem nada a ver com isso!'),
    ('Professor Romerito', 'Aaaah! {player}, saia daqui! Não sei por quanto tempo vou conseguir resistir!'),
    ('Aluno(a)', 'Não vou abandonar o senhor! Vou encontrar uma maneira de derrotar esse vírus e libertar todo mundo!'),
    ('IFVania', 'Resistência detectada. Enviando unidade de combate para neutralizar a ameaça.')
]


AFTER_BOSS_DIALOGUE = [
    ('Aluno(a)', 'Consegui vencer esse combate! Professor, o senhor está bem?'),
    ('Professor Romerito', 'Estou recuperando o controle... Obrigado, {player}. Mas a IFVania ainda está conectada aos sistemas da escola.'),
    ('Aluno(a)', 'Então a batalha ainda não acabou. Precisamos chegar ao quadro de energia antes que ela corrompa mais pessoas.'),
    ('Professor Romerito', 'Isso mesmo. Continue em frente e não confie em tudo o que aparecer nas telas. A IFVania pode tentar enganar você.'),
    ('Sistema', 'Novo objetivo: encontre a saída e continue sua jornada até o quadro de energia.'),
    ('IFVania', 'Você pode derrotar meus agentes, mas não pode impedir o inevitável. A escola inteira pertence a mim.'),
    ('Aluno(a)', 'Veremos! Enquanto eu puder continuar lutando, ainda existe uma chance de salvar todo mundo.')
]



def build_levels():
    """Mapa fixo com piso contínuo, degraus baixos e arena desobstruída."""
    # Piso acima da caixa de diálogo para manter Romerito visível na conversa.
    width, height, ground = 56, 17, 11
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for x in range(width):
        grid[0][x] = '#'
        for y in range(ground, height):
            grid[y][x] = '#'
    for y in range(height):
        grid[y][0] = grid[y][-1] = '#'
    # Obstáculos de 32 ou 64 pixels, abaixo do alcance do salto básico.
    for left, right, rise in ((10, 13, 1), (18, 21, 2), (27, 29, 1)):
        for x in range(left, right):
            for y in range(ground-rise, ground):
                grid[y][x] = '#'
    grid[ground-1][2] = 'P'
    for x in (7, 16, 24, 32):
        grid[ground-1][x] = 'E'
    grid[ground-1][38] = 'D'
    grid[ground-2][49] = 'B'
    grid[ground-1][54] = 'X'
    boss = dict(BOSS_DEFS[0], subject='Mundo virtual')
    return [{
        'index': 0,
        'name': 'Fase 1: Mundo virtual',
        'ascii_map': [''.join(row) for row in grid],
        'boss': boss,
        'ability_reward': None,
        'boss_dialogue': REUNION_DIALOGUE,
        'victory_dialogue': AFTER_BOSS_DIALOGUE,
        'requires_infection': True,
        'school_battle': True,
        'cinematic_transform': True,
        'clear_encounter_on_defeat': True,
        'arena_left': 38 * TILE_SIZE,
    }]
