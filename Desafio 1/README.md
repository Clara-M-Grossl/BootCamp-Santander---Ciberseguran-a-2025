# Desafio Prático: Teste de Brute Force

**Projeto do Bootcamp Santander — Cibersegurança 2025 (DIO)**

---

### Visão Geral

Este projeto é um exercício prático de **Pentest (Teste de Intrusão)** focado na técnica de **Força Bruta (Brute Force)**. O objetivo foi configurar um ambiente de laboratório isolado para **auditar vulnerabilidades de autenticação** utilizando as ferramentas **Medusa** e **Hydra** do Kali Linux.

A documentação abaixo detalha a execução bem-sucedida do ataque contra diferentes serviços (FTP, HTTP/Web e SMB) em um alvo vulnerável, e as principais lições aprendidas sobre **mitigação**.

**Atenção:** Todos os testes foram realizados em **Máquinas Virtuais (VMs) isoladas** dentro de um ambiente controlado (VirtualBox). A execução destes testes em qualquer sistema sem autorização explícita é ilegal e antiética.

---

### Ambiente de Laboratório

Para garantir um teste seguro e replicável:

* **Host:** VirtualBox
* **Atacante (Scanner):** **Kali Linux**
* **Alvo (Target):** **Metasploitable 2** (IP: `192.168.56.101`)
* **Rede:** Configuração **Host-only** ou **Internal Network** (garantindo que as VMs estivessem em uma rede privada isolada).

#### Ferramentas Chave Utilizadas

| Ferramenta | Uso no Projeto |
| :--- | :--- |
| **Medusa** | Ataques de Força Bruta contra serviços de rede (FTP, SMB). |
| **Hydra** | Ataques de Força Bruta contra formulários web (HTTP-POST-FORM). |
| **nmap** | Enumeração inicial de serviços e portas abertas no alvo. |
| **enum4linux** | Enumeração de usuários e informações do serviço SMB. |

---

### 1.  Enumeração e Descoberta de Serviços

Antes de qualquer ataque, foi realizada a descoberta de serviços para entender o alvo.

* **Comando:** `nmap -sV -p 21,22,80,445,139 192.168.56.101`
* **Resultado:** Identificação de serviços abertos e vulneráveis, como **FTP (vsftpd 2.3.4)**, **SSH**, **HTTP (Apache)** e **SMB/NetBIOS (Samba)**.

---

### 2. Ataque a Serviços de Rede (Medusa)

Utilizando wordlists personalizadas (`users.txt` e `pass.txt`), o Medusa foi usado para testar credenciais fracas em serviços de rede.

#### 2.1 Força Bruta em FTP (Porta 21)

* **Comando:** `medusa -h 192.168.56.101 -U users.txt -P pass.txt -M ftp -t 6`
* **Sucesso Encontrado:** Credencial **`msfadmin:msfadmin`** foi localizada e validada com o comando `ftp`.

#### 2.2 Password Spraying em SMB (Portas 139/445)

* **Pré-Ataque:** Enumeração de usuários via **`enum4linux`** para obter uma lista de usuários válidos.
* **Comando:** `medusa -h 192.168.56.101 -U smb_users.txt -P senhas_spray.txt -M smbnt -t 2`
* **Sucesso Encontrado:** Credencial **`msfadmin:msfadmin`** foi encontrada e validada via **`smbclient`**, garantindo acesso.

---

### 3. Ataque a Formulário Web (Hydra)

O Hydra foi selecionado por sua eficiência em ataques a formulários web via método `HTTP-POST-FORM` (utilizado pelo DVWA).

* **Alvo:** Formulário de login do **DVWA** (página `/dvwa/login.php`).
* **Comando:** `hydra -L users.txt -P pass.txt 192.168.56.101 http-post-form "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed"`
    * *A "Fail String" (`Login failed`) é crucial para que o Hydra saiba quando a tentativa falhou.*
* **Sucesso Encontrado:** Credencial **`admin:password`** foi localizada com sucesso.

---

### 7. Mitigações Recomendadas contra Força Bruta

O principal aprendizado do desafio é como defender esses serviços. A Força Bruta é uma falha de autenticação que pode ser mitigada com as seguintes práticas:

| Falha de Segurança | Ação de Mitigação |
| :--- | :--- |
| **Senhas Fracas** | Implementar **Política de Senhas Fortes** (tamanho, complexidade, expiração) e incentivar o uso de Gerenciadores de Senha. |
| **Múltiplas Tentativas** | Configurar **Limite de Tentativas de Login** (Rate Limiting) e **Bloqueio de Contas** temporário após X falhas. |
| **Acesso Crítico** | Exigir **Autenticação de Múltiplos Fatores (MFA)** para todos os serviços críticos (SSH, VPN, Web Apps). |
| **Serviços Expostos** | **Desativar serviços desnecessários** (se não usa FTP, desligue-o). Restringir acesso por IP (Firewall). |
| **Formulários Web** | Utilizar **CAPTCHA/reCAPTCHA** após falhas, **CSRF Tokens** e garantir que o site use **HTTPS**. |
