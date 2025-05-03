FROM node:20-alpine AS builder

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de configuração
COPY app/package.json ./
COPY app/next.config.js ./
COPY app/tsconfig.json ./
COPY app/postcss.config.js ./
COPY app/tailwind.config.ts ./

# Copiar o código fonte
COPY app/app ./app
COPY app/components ./components
COPY app/hooks ./hooks
COPY app/lib ./lib
COPY app/public ./public

# Instalar dependências
RUN npm install

# Copiar o package.json global para ter acesso a todas as dependências
COPY app/global_package.json ./package.json
RUN npm install

# Construir a aplicação
RUN npm run build

# Estágio de produção
FROM node:20-alpine AS runner
WORKDIR /app

# Definir variáveis de ambiente
ENV NODE_ENV production

# Criar usuário não-root para segurança
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copiar arquivos necessários do estágio de construção
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Definir usuário não-root
USER nextjs

# Expor a porta que a aplicação utilizará
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["node", "server.js"]
