# AI Coding and Reviewer Agents

## Usage

## Project Settings

### Settings -> Actions -> General -> Workflow permissions

* Read and write permissions
* ✔ Allow GitHub Actions to create and approve pull requests

![image](https://github.com/user-attachments/assets/e78e60d0-9e16-425e-bcad-264c8f81b878)

### Settings -> Secrets and variables -> Actions -> Secrets

Set `MODEL_API_KEY` and `MODEL_ID`

## Workflow Configuration

Create a file `.github/workflows/ai-agent.yaml`:

```yaml
name: AI Agent Workflow

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]

jobs:
  ai-agents:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Coding Agent (start new task)
        if: github.event_name == 'issues'
        uses: Addefan/coding-agent-megaschool-2026@v1.0.1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model_api_key: ${{ secrets.MODEL_API_KEY }}
          model_id: ${{ secrets.MODEL_ID }}
          mode: "coder"
          issue_number: ${{ github.event.issue.number }}

      - name: Reviewer Agent (review PR)
        if: github.event_name == 'pull_request'
        uses: Addefan/coding-agent-megaschool-2026@v1.0.1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model_api_key: ${{ secrets.MODEL_API_KEY }}
          model_id: ${{ secrets.MODEL_ID }}
          mode: "reviewer"
          pr_number: ${{ github.event.pull_request.number }}
      
      - name: Coding Agent (fix after review)
        if: github.event_name == 'issue_comment' && github.issue.pull_request
        uses: Addefan/coding-agent-megaschool-2026@v1.0.1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model_api_key: ${{ secrets.MODEL_API_KEY }}
          model_id: ${{ secrets.MODEL_ID }}
          mode: "coder"
          pr_number: ${{ github.event.issue.number }}
```

## Отчёт

Пример результата работы агентов (во время разработки):

1. Созданная пользователем Issue - https://github.com/Addefan/megaschool-test-v1/issues/1
2. Созданный Coder Agent'ом PR - https://github.com/Addefan/megaschool-test-v1/pull/4  
В нём соответственно находятся коммиты кодинг-агента и текст изменений в PR
Также в этом же PR находится комментарий от агента-ревьюера, который оставил его после ревью
На всё это использовалась моделька https://openrouter.ai/arcee-ai/trinity-large-preview:free

В этом репозитории-примере все действия выполнялись вручную с помощью CLI, т.е. с помощью команд `uv run main.py --mode coder --issue 1`, `uv run main.py --mode reviewer --pr 4` и `uv run main.py --mode coder --pr 4`.


Репозиторий с демонстрации: https://github.com/Addefan/megaschool-test-v3  
В теории, как я говорил, последовательность действий, описанная выше, должна была сработать автоматически, если бы успел решить баг, из-за которого падала джоба с кодером до его запуска, как я говорил в видео (думаю это связано с изменением воркдира ворклоу).

Из того, что планировалось, но не успел:  
* работа с тестами: проверка, запуск, дописывание (пытался дать права, но моделька совсем с ума сходила, возможно с топовой моделью бы сработало)
* учёт лимита итераций ревью: планировал через HTML-комментарий вести подсчёт итераций, читать его до работы модели и останавливать процесс, когда limit exceeded, но перешёл к деплою, потому что чувствовал что могу не успеть
* хотел подключить Langfuse, как на практике, добавить его в docker-compose, связать с переменной настроек `DEBUG`, но в течение разработки мне для дебага хватало `agent.print_response`, который у меня вызывается в `if __name__ == "__main__"` в файлах агентов, поэтому отложил на конец, на случай, если останется время
* ну и не успел разрешить все проблемы с джобой, потому что это были незапланированные баги под самый конец времени (при локальном запуске контейнера всё срабатывает отлично)

В остальном получился достаточно чистый код, как мне кажется, да и я в принципе на каждом этапе проводил ручное тестирование (те же `if __name__ == "__main__"` есть почти в каждом `.py` файле)

---

Ещё заметил, что забыл закоммитить и запушить `.env.example` до записи демонтации (его вроде в ней должно быть видно). Поэтому распишу чуть поподробнее назначение переменных для локального запуска

* `ёMODEL_BASE_URL`, `MODEL_API_KEY`, `MODEL_ID` - базовые переменные для подключения к модели, URL можно не указывать - по умолчанию OpenRouter URL
* `GITHUB_TOKEN` - access_token пользователя, нужны права на репозиторий, в котором будут работать агенты, но конкретные права сказать не могу - их в списке очень много, времени не было, я выбрал все 
* `GITHUB_WORKSPACE` - локальный путь к склонированному git-репозиторию проекта, в котором будут работать агенты 
* `GITHUB_REPOSITORY` - владелец+название репозитория через слеш, как в демонстрации `Addefan/megaschool-test-v3`

Все три GitHub-переменных во время работы Workflow предоставляются самим GitHub'ом, поэтому в secrets репозитория при демонстрации они не создавались, нужны только для локального тестирования
