FROM httpd:2.4
RUN apt-get update && \
    apt-get install -y vim && \
    apt-get install -y libdbi-perl && \
    apt-get install -y libdbd-pg-perl && \
    apt-get install -y libcgi-pm-perl

RUN mkdir /usr/local/apache2/admin

COPY files/cgi/* /usr/local/apache2/admin/
COPY files/httpd.conf /usr/local/apache2/conf/

#RUN rm -rf /usr/local/apache2/htdocs
#RUN mv /usr/local/apache2/admin /usr/local/apache2/htdocs

#RUN mv /usr/local/apache2/cgi-bin /usr/local/apache2/cgi-bin.old
#RUN mv /usr/local/apache2/admin /usr/local/apache2/cgi-bin

ENV TZ=Europe/Stockholm

#RUN sed -i 's/#\(LoadModule cgid_module modules\/mod_cgid.so\)/\1/' /usr/local/apache2/conf/httpd.conf
#RUN echo 'FallbackResource /' >> /usr/local/apache2/conf/httpd.conf
#RUN echo 'PassEnv DB_HOST' >> /usr/local/apache2/conf/httpd.conf
#RUN echo 'PassEnv DB_PORT' >> /usr/local/apache2/conf/httpd.conf
#RUN echo 'PassEnv DB_NAME' >> /usr/local/apache2/conf/httpd.conf
#RUN echo 'PassEnv DB_USER' >> /usr/local/apache2/conf/httpd.conf
#RUN echo 'PassEnv DB_USER' >> /usr/local/apache2/conf/httpd.conf

