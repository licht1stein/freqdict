# Freqdict: Руководство пользователя для macOS

Freqdict — программа для создания частотного словаря из ваших текстов с автоматической лемматизацией русских слов.

## Что делает программа

- Читает файлы `.txt`, `.md`, `.org`, `.doc`, `.docx`
- Приводит слова к начальной форме (лемматизация): «бежал», «бегу», «бежит» → «бежать»
- Подсчитывает частоту каждого слова
- Убирает служебные слова (предлоги, союзы, частицы, местоимения)
- Сохраняет результат в CSV-файл

## Установка

Откройте Terminal (Терминал) и выполните команду:

```bash
curl -fsSL https://raw.githubusercontent.com/licht1stein/freqdict/v0.13/install-mac.sh | sh
```

Установщик автоматически:
1. Установит `uv` (менеджер Python-пакетов)
2. Установит `antiword` через Homebrew (для чтения `.doc` файлов)
3. Скачает скрипт `freqdict.py`
4. Добавит действие в контекстное меню Finder

**Требование:** На компьютере должен быть установлен [Homebrew](https://brew.sh/).

## Использование

### Способ 1: Через контекстное меню (рекомендуется)

1. Откройте Finder
2. Найдите папку с текстовыми файлами
3. Кликните правой кнопкой мыши на папке
4. Выберите **Services** (Службы) → **Freqdict Here**
5. Дождитесь уведомления об окончании
6. Файл `frequency_dict.csv` откроется автоматически

### Способ 2: Через Terminal

```bash
# Обработать одну папку
uv run ~/.local/share/freqdict/freqdict.py ~/Documents/мои-тексты/

# Обработать текущую папку
cd ~/Documents/мои-тексты/
uv run ~/.local/share/freqdict/freqdict.py .

# Обработать один файл
uv run ~/.local/share/freqdict/freqdict.py документ.docx
```

## Результат

Программа создаёт файл `frequency_dict.csv` в обработанной папке:

```csv
lemma,frequency
человек,62
амортизация,51
энергия,37
психологический,37
атака,35
...
```

Файл можно открыть в Excel, Numbers или Google Sheets.

## Поддерживаемые форматы

| Формат | Описание |
|--------|----------|
| `.txt` | Обычный текст |
| `.md`  | Markdown |
| `.org` | Emacs Org-mode |
| `.doc` | Microsoft Word 97-2003 |
| `.docx`| Microsoft Word 2007+ |

## Решение проблем

### «command not found: uv»
Перезапустите Terminal или выполните:
```bash
source ~/.local/bin/env
```

### «antiword not installed»
Установите antiword:
```bash
brew install antiword
```

### «No supported files found»
Убедитесь, что в папке есть файлы с поддерживаемыми расширениями (.txt, .md, .org, .doc, .docx).

### Неправильная кодировка в .doc файлах
Программа автоматически определяет кодировку (UTF-8 или CP1251). Если текст отображается некорректно, попробуйте пересохранить файл в формате .docx.

## Обновление

Для обновления до последней версии выполните команду установки повторно:

```bash
curl -fsSL https://raw.githubusercontent.com/licht1stein/freqdict/v0.13/install-mac.sh | sh
```

## Удаление

```bash
rm -rf ~/.local/share/freqdict
rm -rf ~/Library/Services/Freqdict\ Here.workflow
```
