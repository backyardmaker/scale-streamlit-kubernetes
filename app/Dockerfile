# Set build arguments
ARG APP_DIR=/app
ARG PYTHON_DEP_BUILD_PATH=/dockerbuild
ARG GROUP_NAME=streamlitapp
ARG USER_NAME=appuser
ARG GROUP_ID=1001
ARG USER_ID=1001

#===============
# Build Stage
#===============

# Base image
FROM python:3.12-slim as build-base

ARG PYTHON_DEP_BUILD_PATH

# Copy requirements and install as created user
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache -r requirements.txt --target "${PYTHON_DEP_BUILD_PATH}"

#===============
# Runner Stage
#===============

# Base image
FROM python:3.12-slim

ARG APP_DIR
ARG PYTHON_DEP_BUILD_PATH
ARG GROUP_NAME
ARG USER_NAME
ARG GROUP_ID
ARG USER_ID

# Create app directory and non-root user
RUN mkdir -p "${APP_DIR}" && \
    groupadd -g ${GROUP_ID} ${GROUP_NAME} && \
    useradd -m -u ${USER_ID} -g ${GROUP_ID} ${USER_NAME}

# Copy source code
COPY app.py ${APP_DIR}/
COPY src/ ${APP_DIR}/src

# Copy python dependencies
COPY --from=build-base ${PYTHON_DEP_BUILD_PATH} /usr/local/lib/python3.12/
RUN mv /usr/local/lib/python3.12/bin/* /usr/local/bin && \
    # Verify streamlit exec correctly configured
    which streamlit

# Set working directory
WORKDIR ${APP_DIR}

# Change ownership to non-root user
RUN chown -R ${USER_ID}:${GROUP_ID} ${APP_DIR}

# Expose streamlit port
EXPOSE 8501

# Switch to non-root user
USER ${USER_ID}:${GROUP_ID}

# Set default executable
ENTRYPOINT ["streamlit", "run", "app.py"]