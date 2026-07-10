# Assets - Sistema de Análise de Sentimentos

Esta pasta contém os arquivos SVG animados usados na documentação do projeto.

## 📁 Arquivos

### 1. `system-overview.svg`
**Descrição:** Visão geral do sistema em tempo real

**Uso:** Mostrar o fluxo completo desde o usuário até o dashboard

**Local:** README.md (seção Visão Geral)

**Animações incluídas:**
- Pulso nos componentes (API, Dashboard)
- Fluxo de dados animado entre componentes
- Gráfico de barras animado no dashboard
- Indicador "LIVE" piscando
- Partículas decorativas

---

### 2. `architecture-diagram.svg`
**Descrição:** Diagrama arquitetural completo

**Uso:** Ilustrar a arquitetura em camadas do sistema

**Local:** README.md (seção Arquitetura)

**Camadas mostradas:**
1. Fontes de Dados (Twitter, Google, CSV, API)
2. Pré-processamento (Limpeza, Tokenização, Normalização)
3. Modelos PLN (VADER, BERT, LLM)
4. Saída (JSON)
5. Dashboard + Database

**Animações incluídas:**
- Flow arrows entre camadas
- Pulse nos modelos
- Spin no loading indicator
- Float suave nos componentes

---

### 3. `analysis-flow.svg`
**Descrição:** Fluxo detalhado de análise de um texto

**Uso:** Mostrar o processo passo-a-passo de uma análise

**Local:** README.md (seção Fluxo de Análise)

**Elementos:**
- Entrada de texto (efeito typewriter)
- Pipeline: Clean → Tokenize → Analyze → Score
- Resultado com emoji animado
- Barras de distribuição animadas
- Tempo de processamento

**Animações incluídas:**
- Cursor piscando (typewriter)
- Wave nas etapas do pipeline
- Glow no resultado
- Bar animation no gráfico

---

### 4. `realtime-dashboard.svg`
**Descrição:** Dashboard completo com métricas em tempo real

**Uso:** Mostrar a interface do dashboard

**Local:** README.md (seção Dashboard)

**Componentes:**
- Header com Live Badge
- Cards de métricas (Total, Média, Tempo, Erros)
- Gráfico de linha temporal (evolução)
- Donut chart (distribuição)
- Tabela de últimas análises

**Animações incluídas:**
- Live dot pulsando
- Line chart draw (traçado progressivo)
- Number count pulse
- Barras do gráfico animadas

---

## 🎨 Paleta de Cores

| Cor | Hex | Uso |
|-----|-----|-----|
| Fundo Principal | `#0d1117` | Background |
| Fundo Secundário | `#1a1a2e` | Cards |
| API Gradient | `#667eea` → `#764ba2` | Componentes API |
| Modelo Gradient | `#11998e` → `#38ef7d` | Componentes Models |
| Dashboard Gradient | `#fc4a1a` → `#f7b733` | Dashboard |
| Positivo | `#38ef7d` | Sentimento positivo |
| Neutro | `#f7b733` | Sentimento neutro |
| Negativo | `#fc4a1a` | Sentimento negativo |

---

## 🔧 Editando SVGs

Para editar os SVGs:

1. Use um editor de texto (VS Code, Notepad++)
2. As animações CSS estão inline no `<defs><style>`
3. Coordenadas e cores podem ser ajustadas diretamente
4. Teste no navegador após editar

### Ferramentas Recomendadas

- **SVG Editor Online:** [SVGViewer](https://www.svgviewer.dev/)
- **Desktop:** Inkscape (gratuito), Adobe Illustrator
- **VS Code Extension:** SVG Viewer

---

## 📊 Performance

Os SVGs são otimizados para:

- **Tamanho:** < 50KB cada
- **Animações:** CSS-only (GPU accelerated)
- **Compatibilidade:** Navegadores modernos
- **Acessibilidade:** Texto legível, contrastes adequados

---

## 📝 Notas

- Todos os textos estão em português brasileiro
- Emojis são renderizados como texto Unicode
- Animações podem ser desativadas via `prefers-reduced-motion` (não implementado)
- Para dark mode, use fundo escuro no container

---

**Autor:** Sistema de Análise de Sentimentos  
**Data:** 2026-07-10  
**Versão:** 0.1.0