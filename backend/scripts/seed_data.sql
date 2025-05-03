-- Script para popular o banco de dados HUMANIQ com dados de exemplo

-- Inserir usuários de exemplo
-- Senhas: 'senha123' (hash gerado com werkzeug.security.generate_password_hash)
INSERT INTO users (name, email, password_hash, created_at, points, level) VALUES
('João Silva', 'joao@exemplo.com', 'pbkdf2:sha256:600000$7xMnaBqJbGTVDYw4$c9e52532647f8b5d3a0d7fc805c9e85fbc2cd9e6c9de2fbe5fdb9d9898d69a3b', datetime('now', '-30 days'), 150, 2),
('Maria Oliveira', 'maria@exemplo.com', 'pbkdf2:sha256:600000$7xMnaBqJbGTVDYw4$c9e52532647f8b5d3a0d7fc805c9e85fbc2cd9e6c9de2fbe5fdb9d9898d69a3b', datetime('now', '-25 days'), 80, 1),
('Pedro Santos', 'pedro@exemplo.com', 'pbkdf2:sha256:600000$7xMnaBqJbGTVDYw4$c9e52532647f8b5d3a0d7fc805c9e85fbc2cd9e6c9de2fbe5fdb9d9898d69a3b', datetime('now', '-15 days'), 220, 3);

-- Inserir avaliações de habilidades
INSERT INTO skill_assessments (user_id, communication, active_listening, conflict_resolution, teamwork, critical_thinking, time_management, assessment_date) VALUES
(1, 3, 4, 2, 5, 3, 4, datetime('now', '-29 days')),
(1, 4, 4, 3, 5, 4, 4, datetime('now', '-15 days')),
(2, 2, 3, 2, 4, 3, 2, datetime('now', '-24 days')),
(3, 5, 4, 4, 5, 5, 3, datetime('now', '-14 days'));

-- Inserir desafios
INSERT INTO challenges (title, description, skill_type, challenge_type, content, points) VALUES
('Comunicação Efetiva', 'Aprenda a se comunicar de forma clara e eficaz em diferentes contextos', 'comunicacao', 'video', 'https://www.youtube.com/watch?v=exemplo1', 10),
('Escuta Ativa na Prática', 'Desenvolva sua capacidade de escutar ativamente durante conversas', 'escuta_ativa', 'quiz', '{"perguntas":[{"pergunta":"Qual é o principal objetivo da escuta ativa?","opcoes":["Responder rapidamente","Entender completamente a mensagem","Interromper quando necessário","Demonstrar superioridade"],"resposta_correta":1}]}', 15),
('Resolução de Conflitos', 'Aprenda técnicas para mediar e resolver conflitos de forma construtiva', 'resolucao_conflitos', 'practice', 'Simule uma situação de conflito com um colega e aplique as técnicas aprendidas', 20),
('Trabalho em Equipe', 'Desenvolva habilidades para trabalhar de forma colaborativa', 'trabalho_equipe', 'video', 'https://www.youtube.com/watch?v=exemplo2', 10),
('Pensamento Crítico', 'Aprenda a analisar informações e tomar decisões baseadas em evidências', 'pensamento_critico', 'quiz', '{"perguntas":[{"pergunta":"O que caracteriza o pensamento crítico?","opcoes":["Aceitar informações sem questionar","Analisar evidências antes de formar opinião","Seguir a opinião da maioria","Decidir rapidamente"],"resposta_correta":1}]}', 15),
('Gestão do Tempo', 'Técnicas para organizar seu tempo e aumentar a produtividade', 'gestao_tempo', 'practice', 'Crie um plano de estudos semanal aplicando as técnicas de gestão do tempo', 20);

-- Inserir resultados de desafios
INSERT INTO challenge_results (user_id, challenge_id, completed, score, feedback, completed_at) VALUES
(1, 1, TRUE, NULL, 'Aprendi muito sobre comunicação efetiva!', datetime('now', '-28 days')),
(1, 2, TRUE, 90, NULL, datetime('now', '-26 days')),
(1, 3, TRUE, NULL, 'Foi desafiador, mas consegui aplicar as técnicas.', datetime('now', '-20 days')),
(2, 1, TRUE, NULL, 'Vídeo muito esclarecedor.', datetime('now', '-23 days')),
(2, 4, TRUE, NULL, 'Gostei das dicas de trabalho em equipe.', datetime('now', '-20 days')),
(3, 1, TRUE, NULL, 'Excelente conteúdo!', datetime('now', '-13 days')),
(3, 2, TRUE, 100, NULL, datetime('now', '-12 days')),
(3, 5, TRUE, 85, NULL, datetime('now', '-10 days'));

-- Inserir badges
INSERT INTO badges (name, description, image_url, requirement) VALUES
('Comunicador Iniciante', 'Completou o primeiro desafio de comunicação', '/static/badges/comunicador_iniciante.png', 'Completar o desafio "Comunicação Efetiva"'),
('Mestre da Escuta', 'Obteve pontuação máxima no quiz de escuta ativa', '/static/badges/mestre_escuta.png', 'Obter 100% no quiz "Escuta Ativa na Prática"'),
('Pacificador', 'Completou o desafio de resolução de conflitos', '/static/badges/pacificador.png', 'Completar o desafio "Resolução de Conflitos"'),
('Colaborador', 'Completou o desafio de trabalho em equipe', '/static/badges/colaborador.png', 'Completar o desafio "Trabalho em Equipe"'),
('Pensador Crítico', 'Obteve boa pontuação no quiz de pensamento crítico', '/static/badges/pensador_critico.png', 'Obter pelo menos 80% no quiz "Pensamento Crítico"'),
('Organizador do Tempo', 'Completou o desafio de gestão do tempo', '/static/badges/organizador_tempo.png', 'Completar o desafio "Gestão do Tempo"');

-- Atribuir badges aos usuários
INSERT INTO user_badges (user_id, badge_id) VALUES
(1, 1), -- João ganhou o badge "Comunicador Iniciante"
(1, 3), -- João ganhou o badge "Pacificador"
(2, 1), -- Maria ganhou o badge "Comunicador Iniciante"
(2, 4), -- Maria ganhou o badge "Colaborador"
(3, 1), -- Pedro ganhou o badge "Comunicador Iniciante"
(3, 2), -- Pedro ganhou o badge "Mestre da Escuta"
(3, 5); -- Pedro ganhou o badge "Pensador Crítico"

-- Inserir posts no fórum
INSERT INTO forum_posts (user_id, title, content, created_at) VALUES
(1, 'Dicas para melhorar a comunicação', 'Olá pessoal! Gostaria de compartilhar algumas dicas que me ajudaram a melhorar minha comunicação...', datetime('now', '-25 days')),
(2, 'Como lidar com conflitos no trabalho?', 'Estou enfrentando alguns conflitos no meu estágio e gostaria de saber como vocês lidam com situações assim...', datetime('now', '-18 days')),
(3, 'Técnicas de gestão do tempo que funcionam', 'Depois de completar o desafio de gestão do tempo, comecei a aplicar algumas técnicas que realmente funcionaram para mim...', datetime('now', '-8 days'));

-- Inserir comentários no fórum
INSERT INTO forum_comments (post_id, user_id, content, created_at) VALUES
(1, 2, 'Obrigada pelas dicas, João! Vou tentar aplicar no meu dia a dia.', datetime('now', '-24 days')),
(1, 3, 'Excelentes dicas! Também recomendo praticar apresentações em frente ao espelho.', datetime('now', '-23 days')),
(2, 1, 'Maria, já passei por isso. O que me ajudou foi conversar diretamente com a pessoa, mas de forma calma e objetiva.', datetime('now', '-17 days')),
(2, 3, 'Concordo com o João. Comunicação direta, mas respeitosa, é a chave.', datetime('now', '-16 days')),
(3, 1, 'Pedro, quais técnicas funcionaram melhor para você?', datetime('now', '-7 days')),
(3, 2, 'Estou tentando implementar a técnica Pomodoro, mas ainda tenho dificuldades. Alguma dica?', datetime('now', '-6 days'));

-- Inserir certificados
INSERT INTO certificates (user_id, title, description, issue_date) VALUES
(1, 'Comunicação Efetiva', 'Certificado de conclusão do módulo de Comunicação Efetiva', datetime('now', '-20 days')),
(3, 'Escuta Ativa', 'Certificado de conclusão do módulo de Escuta Ativa com excelência', datetime('now', '-10 days'));
