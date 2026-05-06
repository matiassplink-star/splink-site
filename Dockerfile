FROM nginx:alpine

# Copia todos os arquivos do projeto para o diretório do Nginx
COPY . /usr/share/nginx/html/

# Remove arquivos desnecessários que não devem ir para o ar
RUN rm -rf /usr/share/nginx/html/.git /usr/share/nginx/html/apply_seo.py /usr/share/nginx/html/temp_seo.txt

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
