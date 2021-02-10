FROM       ruby:2.3.1

# The location of the gena server api in the image
ENV        APP_HOME=/usr/src/app/
WORKDIR    $APP_HOME

# Copy the Gemfile and Gemfile.lock to make them more likely out of the way when the build cache is invalidated
COPY       ./Gemfile* ./
RUN        bundle install

# Install locale and other stuff
RUN        DEBIAN_FRONTEND=noninteractive \
           apt-get update \
        && apt-get install -y --no-install-recommends \
           vim mc tree less  \
           postgresql-client \
           locales \
        && rm -rf /var/lib/apt/lists/* \
        && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
        && locale-gen \
        && cp /usr/share/zoneinfo/Europe/Stockholm /etc/localtime

# Prepare the environment
ENV        LANG=en_US.UTF-8
ENV        LANGUAGE=en_US:en
ENV        RAILS_LOG_TO_STDOUT=true

# Copy the full context
COPY       . ./

# Add a script to be executed every time the container starts
COPY       entrypoint.sh /
RUN        chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Start the main process
CMD        ["bundle", "exec", "rails", "server",  "-b", "0.0.0.0", "-e", "${RAILS_ENV}"]

