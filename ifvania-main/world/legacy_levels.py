"""Campanha antiga, fora do menu principal. Definição das 6 fases: mapas (gerados proceduralmente de forma determinística),
professores-chefe, textos de diálogo e habilidades concedidas.
"""
import random
from entities.boss import BOSS_DEFS
from powerups import Ability

LENGTHS = [46, 52, 58, 64, 70, 78]
GROUND_ROW = 14
HEIGHT_TILES = 17


def _generate_rows(length_tiles, height_tiles, ground_row, seed, num_enemies):
    rng = random.Random(seed)
    grid = [['.' for _ in range(length_tiles)] for _ in range(height_tiles)]

    # bordas do nível
    for x in range(length_tiles):
        grid[0][x] = '#'
        grid[height_tiles - 1][x] = '#'
    for y in range(height_tiles):
        grid[y][0] = '#'
        grid[y][length_tiles - 1] = '#'

    # chão principal, com pequenos degraus e vãos de 1 bloco (sempre pulável)
    x = 1
    row = ground_row
    while x < length_tiles - 1:
        grid[row][x] = '#'
        x += 1
        if x > 10 and x < length_tiles - 12 and rng.random() < 0.10:
            # vão pequeno (1 bloco) - sempre transponível a pé
            x += 1
        elif x > 8 and x < length_tiles - 10 and rng.random() < 0.12:
            # degrau de 1 bloco de altura
            row = max(ground_row - 2, min(ground_row + 1, row + rng.choice([-1, 1])))

    # espinhos ocasionais sobre o chão
    for x in range(4, length_tiles - 12):
        if grid[ground_row][x] == '#' and rng.random() < 0.05:
            grid[ground_row - 1][x] = '^'

    # plataformas flutuantes decorativas / rotas alternativas
    for _ in range(length_tiles // 8):
        px = rng.randint(6, length_tiles - 14)
        py = rng.randint(3, ground_row - 3)
        plen = rng.randint(2, 4)
        for k in range(plen):
            if px + k < length_tiles - 1:
                grid[py][px + k] = '#'

    # Arena livre, com piso plano desde a entrada do encontro. Apenas adicionar
    # piso deixava blocos do terreno anterior sobrepondo o chefe e seus tiros.
    for gx in range(length_tiles - 12, length_tiles - 1):
        for gy in range(1, height_tiles - 1):
            grid[gy][gx] = '#' if gy >= ground_row else '.'

    # inimigos comuns espalhados pelo chão principal
    enemy_positions = sorted(rng.sample(range(6, length_tiles - 14), min(num_enemies, max(1, length_tiles - 20))))
    for ex in enemy_positions:
        grid[ground_row - 1][ex] = 'E'

    # jogador
    grid[ground_row - 1][2] = 'P'

    # gatilho de diálogo antes do chefe
    dialogue_x = length_tiles - 12
    grid[ground_row - 1][dialogue_x] = 'D'

    # chefe
    boss_x = length_tiles - 6
    grid[ground_row - 2][boss_x] = 'B'

    # saída (só ativa após derrotar o chefe)
    exit_x = length_tiles - 2
    grid[ground_row - 1][exit_x] = 'X'

    return [''.join(r) for r in grid], boss_x, ground_row


def build_legacy_levels():
    levels = []
    for i, boss_def in enumerate(BOSS_DEFS):
        length = LENGTHS[i]
        rows, boss_x_tile, ground_row = _generate_rows(
            length_tiles=length,
            height_tiles=HEIGHT_TILES,
            ground_row=GROUND_ROW,
            seed=1000 + i * 37,
            num_enemies=3 + i,
        )
        levels.append({
            "index": i,
            "name": f"Fase {i + 1}: {boss_def['subject']}",
            "ascii_map": rows,
            "boss": boss_def,
            "ability_reward": ABILITY_ORDER[i],
            "intro_dialogue": INTRO_DIALOGUES[i],
            "boss_dialogue": BOSS_DIALOGUES[i],
            "victory_dialogue": VICTORY_DIALOGUES[i],
        })
    return levels


ABILITY_ORDER = [
    Ability.DOUBLE_JUMP,
    Ability.DASH,
    Ability.WALL_CLIMB,
    Ability.RANGED_SHOT,
    Ability.SHIELD,
    None,  # o chefe final não concede novo poder, apenas encerra o jogo
]


INTRO_DIALOGUES = [
    [("Aluno(a)", "A Sala de Iniciação parece... estranhamente colorida."),
     ("RomerBug", "Finalmente chegou! A aula começa de terno, mas eu também treino para correr!"),
     ("Aluno(a)", "Espera... por que tem um vírus usando roupa de professor?"),
     ("RomerBug", "Vírus? Prefiro o termo especialista em reprovação!"),
     ("Aluno(a)", "Certo. Isso não é nada assustador. Nada mesmo.")],

    [("Aluno(a)", "Esse laboratório está silencioso demais. Até as cobras parecem estar esperando alguma coisa."),
     ("Prof. Python", "Finalmente chegou! Preparei um ambiente de execução especialmente para você."),
     ("Aluno(a)", "E por que tem uma mensagem dizendo que minha chance de aprovação é zero?"),
     ("Prof. Python", "Porque qualquer erro pode ser fatal... para sua nota, é claro."),
     ("Aluno(a)", "Ótimo. Trouxe meu código, minha coragem e um plano B."),
     ("Prof. Python", "E qual seria o plano B?"),
     ("Aluno(a)", "Descobrir o plano A durante a luta!")],

    [("Aluno(a)", "A sala de POO está cheia de heranças. Espero que pelo menos alguma venha com dinheiro."),
     ("Prof. Java", "public class VoceVaiPerder extends Aluno { }"),
     ("Aluno(a)", "Essa classe nem implementa um método de vitória!"),
     ("Prof. Java", "Não se preocupe. Seu programa será encerrado antes disso."),
     ("Aluno(a)", "Então vamos ver quem vai receber um NullPointerException primeiro!")],

    [("Aluno(a)", "Esse lugar cheira a ponteiro solto e memória vazando. Acho que preciso de um antivírus."),
     ("Prof. C", "Segmentation fault... na sua coragem!"),
     ("Aluno(a)", "Você já tentou liberar essa quantidade de arrogância com free()?"),
     ("Prof. C", "Cuidado com o que fala, aluno. Um erro de memória pode custar caro."),
     ("Aluno(a)", "E um erro de cálculo pode custar uma derrota. Vamos descobrir!")],

    [("Aluno(a)", "Essa biblioteca está organizada demais. Tenho certeza de que tem alguma coisa errada."),
     ("Prof. SQL", "SELECT * FROM alunos WHERE coragem > 0; -- 0 linhas retornadas."),
     ("Aluno(a)", "Engraçado. Acho que sua consulta está com defeito."),
     ("Prof. SQL", "Impossível! Meu banco de dados nunca erra."),
     ("Aluno(a)", "Então vamos fazer um JOIN entre sua confiança e a realidade!")],

    [("Aluno(a)", "O núcleo do sistema... então era daqui que o vírus controlava a escola."),
     ("Prof. Assembly", "MOV medo, TODOS_OS_REGISTRADORES"),
     ("Aluno(a)", "Você corrompeu as aulas, os laboratórios e até os professores!"),
     ("Prof. Assembly", "Ordem, precisão e controle. Não há espaço para falhas."),
     ("Aluno(a)", "Você esqueceu de incluir uma variável: minha persistência."),
     ("Prof. Assembly", "Então que comece o último processamento.")],
]


BOSS_DIALOGUES = [
    [("RomerBug", "Prepare-se para a prova... e para meus aviões de papel!"),
     ("Aluno(a)", "Você transformou a escola inteira em uma prova surpresa!"),
     ("RomerBug", "A educação exige sacrifícios!"),
     ("Aluno(a)", "Acho que você confundiu ensinar com aterrorizar!"),
     ("RomerBug", "Quando minha vida chegar à metade, você vai conhecer o SpeedBug!"),
     ("Aluno(a)", "Mais um professor com segunda forma? Eu devia ter estudado para outra coisa!")],

    [("Prof. Python", "Vamos ver se você consegue manter a lógica sob pressão!"),
     ("Aluno(a)", "Pode mandar! Já sobrevivi a erros que nem eu sabia explicar!"),
     ("Prof. Python", "Seu código está cheio de falhas!"),
     ("Aluno(a)", "E o seu plano de aula está cheio de más intenções!")],

    [("Prof. Java", "Prepare-se para um NullPointerException de dor."),
     ("Aluno(a)", "Você fala difícil para esconder que está perdendo?"),
     ("Prof. Java", "Minha arquitetura é perfeita!"),
     ("Aluno(a)", "Então por que sua defesa está cheia de brechas?")],

    [("Prof. C", "Cuidado com o buffer overflow dos meus ataques."),
     ("Aluno(a)", "E você tome cuidado com a minha capacidade de adaptação!"),
     ("Prof. C", "Um único erro e tudo desmorona!"),
     ("Aluno(a)", "Ainda bem que aprendi a não desistir no primeiro erro!")],

    [("Prof. SQL", "Isso é um DELETE FROM sua_paciencia;"),
     ("Aluno(a)", "Pode executar quantas vezes quiser. Minha paciência tem backup!"),
     ("Prof. SQL", "Vou apagar todas as suas chances de vitória!"),
     ("Aluno(a)", "Então está na hora de recuperar os dados e encerrar essa consulta!")],

    [("Prof. Assembly", "Sem abstrações. Só você, eu e registradores."),
     ("Aluno(a)", "Passei por cinco professores para chegar até você."),
     ("Prof. Assembly", "Sua persistência não altera o resultado previsto."),
     ("Aluno(a)", "Engraçado. O sistema também previa que eu perderia as outras batalhas."),
     ("Prof. Assembly", "Então provarei que sua vitória foi apenas uma sequência de exceções."),
     ("Aluno(a)", "Pode preparar o último comando. Eu não vou desistir agora!")],
]


VICTORY_DIALOGUES = [
    [("SpeedBug", "Ufa... você cruzou a linha de chegada. O vírus perdeu!"),
     ("Aluno(a)", "Boa corrida, RomerBug! Da próxima vez, tente ensinar em vez de trapacear."),
     ("RomerBug", "Talvez eu tenha exagerado um pouquinho..."),
     ("Aluno(a)", "Um pouquinho? Você transformou a escola em uma pista de obstáculos!"),
     ("Sistema", "Habilidade adquirida: Pulo Duplo!"),
     ("Aluno(a)", "Agora posso alcançar lugares que antes pareciam impossíveis!")],

    [("Prof. Python", "Meu... código... está... sem exceções..."),
     ("Aluno(a)", "Parece que encontramos um erro na sua estratégia."),
     ("Prof. Python", "Você realmente aprendeu a pensar antes de executar."),
     ("Aluno(a)", "E aprendi que errar faz parte de aprender!"),
     ("Sistema", "Habilidade adquirida: Dash Veloz!"),
     ("Aluno(a)", "Agora posso superar os obstáculos antes mesmo que percebam!")],

    [("Prof. Java", "Fatal Error: professor.encerrar()..."),
     ("Aluno(a)", "Acho que sua hierarquia de poder acabou de perder a classe principal."),
     ("Prof. Java", "Como você conseguiu superar minha arquitetura?"),
     ("Aluno(a)", "Com persistência, prática e um pouco de improviso."),
     ("Sistema", "Habilidade adquirida: Escalada de Parede!"),
     ("Aluno(a)", "Agora nenhum obstáculo vai me impedir de continuar!")],

    [("Prof. C", "Core dumped... foi... uma... boa... aula..."),
     ("Aluno(a)", "Você quase conseguiu me derrubar, professor."),
     ("Prof. C", "Nunca subestime os perigos de um ponteiro mal utilizado..."),
     ("Aluno(a)", "Pode deixar. Vou usar o que aprendi para construir, não destruir."),
     ("Sistema", "Habilidade adquirida: Tiro de Ponteiro!"),
     ("Aluno(a)", "Finalmente posso atingir obstáculos que estão longe de mim!")],

    [("Prof. SQL", "COMMIT; -- fim da transação, aluno..."),
     ("Aluno(a)", "Transação concluída! E dessa vez ninguém perdeu os próprios dados."),
     ("Prof. SQL", "Você conseguiu recuperar o controle do sistema..."),
     ("Aluno(a)", "E aprendi que conhecimento não serve para controlar os outros."),
     ("Sistema", "Habilidade adquirida: Escudo de Dados!"),
     ("Aluno(a)", "Agora estou preparado para proteger a escola no confronto final!")],

    [("Prof. Assembly", "HALT."),
     ("Aluno(a)", "Não. O comando de parada é seu, não meu."),
     ("Prof. Assembly", "Impossível... Você superou todos os protocolos de segurança."),
     ("Aluno(a)", "Aprendi com cada professor, cada erro e cada desafio."),
     ("Prof. Assembly", "O vírus... está perdendo o controle..."),
     ("Aluno(a)", "A escola não é um sistema para você dominar. É um lugar para aprender!"),
     ("Sistema", "Vírus neutralizado. Todos os sistemas restaurados."),
     ("Diretora", "Você conseguiu! A escola está livre, e nossos professores estão recuperando o controle de si mesmos."),
     ("Aluno(a)", "Eu não teria conseguido sem tudo o que aprendi pelo caminho."),
     ("Diretora", "Você provou que conhecimento, coragem e persistência podem superar qualquer desafio."),
     ("Sistema", "Campanha concluída! Obrigado por jogar IFvania!")],
]