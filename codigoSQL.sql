-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.agendamentos (
  id bigint NOT NULL DEFAULT nextval('agendamentos_id_seq'::regclass),
  cliente_id bigint NOT NULL,
  servico_id bigint NOT NULL,
  data_agendamento date NOT NULL,
  horario time without time zone NOT NULL,
  status USER-DEFINED NOT NULL DEFAULT 'pendente'::status_agendamento,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT agendamentos_pkey PRIMARY KEY (id),
  CONSTRAINT agendamentos_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.usuarios(id),
  CONSTRAINT agendamentos_servico_id_fkey FOREIGN KEY (servico_id) REFERENCES public.servicos(id)
);


CREATE TABLE public.avaliacoes (
  id bigint NOT NULL DEFAULT nextval('avaliacoes_id_seq'::regclass),
  cliente_id bigint NOT NULL,
  estabelecimento_id bigint NOT NULL,
  nota integer NOT NULL CHECK (nota >= 1 AND nota <= 5),
  comentario text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT avaliacoes_pkey PRIMARY KEY (id),
  CONSTRAINT avaliacoes_estabelecimento_id_fkey FOREIGN KEY (estabelecimento_id) REFERENCES public.estabelecimentos(id),
  CONSTRAINT avaliacoes_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.usuarios(id)
);


CREATE TABLE public.categorias (
  id bigint NOT NULL DEFAULT nextval('categorias_id_seq'::regclass),
  nome text NOT NULL,
  CONSTRAINT categorias_pkey PRIMARY KEY (id)
);


CREATE TABLE public.estabelecimentos (
  id bigint NOT NULL DEFAULT nextval('estabelecimentos_id_seq'::regclass),
  usuario_id bigint NOT NULL,
  nome_fantasia text NOT NULL,
  cnpj character NOT NULL UNIQUE,
  endereco text NOT NULL,
  telefone text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT estabelecimentos_pkey PRIMARY KEY (id),
  CONSTRAINT estabelecimentos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id)
);


CREATE TABLE public.horarios_funcionamento (
  id bigint NOT NULL DEFAULT nextval('horarios_funcionamento_id_seq'::regclass),
  estabelecimento_id bigint NOT NULL,
  dia_semana USER-DEFINED NOT NULL,
  horario_inicio time without time zone NOT NULL,
  horario_fim time without time zone NOT NULL,
  CONSTRAINT horarios_funcionamento_pkey PRIMARY KEY (id),
  CONSTRAINT horarios_funcionamento_estabelecimento_id_fkey FOREIGN KEY (estabelecimento_id) REFERENCES public.estabelecimentos(id)
);


CREATE TABLE public.servicos (
  id bigint NOT NULL DEFAULT nextval('servicos_id_seq'::regclass),
  estabelecimento_id bigint NOT NULL,
  categoria_id bigint NOT NULL,
  nome text NOT NULL,
  descricao text,
  preco numeric NOT NULL,
  duracao_minutos integer NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT servicos_pkey PRIMARY KEY (id),
  CONSTRAINT servicos_estabelecimento_id_fkey FOREIGN KEY (estabelecimento_id) REFERENCES public.estabelecimentos(id),
  CONSTRAINT servicos_categoria_id_fkey FOREIGN KEY (categoria_id) REFERENCES public.categorias(id)
);


CREATE TABLE public.usuarios (
  id bigint NOT NULL DEFAULT nextval('usuarios_id_seq'::regclass),
  nome text NOT NULL,
  email text NOT NULL,
  senha_hash text NOT NULL,
  tipo USER-DEFINED NOT NULL DEFAULT 'cliente'::user_type,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT usuarios_pkey PRIMARY KEY (id)
);