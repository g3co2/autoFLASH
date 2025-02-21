# Заполняшка + сендлер для кураторов
Автор проекта: [g3co2](https://github.com/g3co2/autoFLASH)

Проект, который за вас будет каждый день в 8:00 по МСК (UTC+3):
1. Отправлять сообщения о дедлайнах в беседу в таком формате![img.png](_images_for_readme/img_5.png)
2. Заполнять журнал (табличку гугл) о сделанных учениками домашках в формате ![img.png](_images_for_readme/img_6.png)

Не потребует от вас знания программирования, но значительно сэкономит ваше время 🢃
## Как использовать?
1. Нужно дублировать этот репозиторий в свой Github. Как это сделать, [смотрите тут](https://qna.habr.com/q/182561).
2. В гугл табличке, где у вас журнал, в 4 строчке последнего столбца должна стоять дата, с которой надо грузить оценки по домашкам (я беру с этой ячейки инфу для понимания того, какие домашки надо выгружать).
3. Далее о самом важно в этом проекте - переменных Github.Secrets, которые нам понадобятся. 
Вся эта штука запускается каждый день благодаря Github.Actions. В файлике
<code>.github/workflows/schedule.yml</code> прописано, что именно должно 
запускаться и во сколько. Также там есть вот эта часть ![тут картинка](_images_for_readme/img.png) 
Здесь в фигурных скобках указаны имена переменных среды на гитхабе. У вашего проекта они должны быть свои. 
Обратите внимание, <mark>все</mark> имена начинаются с <code>secrets.</code>.
Теперь к делу. Заходим в настройки проекта. ![тут картинка](_images_for_readme/img2.png) В колонке настроек слева находим раздел <code>Security -> Secrets and variables -> Actions</code> В итоге должно получиться окошко ниже.
![img.png](_images_for_readme/img_1.png)
Все основные кнопочки тут указаны. Теперь Ваша задача - создать несколько переменных. Вот список и форматы. Прошу также ознакомиться с разделом [Как получить некоторые поля?](https://github.com/g3co2/autoFLASH/tree/master?tab=readme-ov-file#как-получить-некоторые-поля) ниже.
```dotenv
API_DOMAIN=api.домен.ru  # домен сайта с журналом и домашками

# эмейл от вашего аккаунта на сайте с журналом и домашками
API_ACCOUNT_EMAIL=какая_то_почта@домен.noemail
# пароль от вашего аккаунта на сайте с журналом и домашками
API_ACCOUNT_PASSWORD=какиетобуквыицифры

MODULE_ID=0000  # айди текущего блока

# токен от апи группы вконтакте
VK_API_TOKEN=очень_длинная_строчка
VK_GROUP_ID=000000000   # айди группы вконтакте

# айдишник гугл таблички с журналом
GOOGLE_TABLE_ID=буквыцифры
YOUR_GOOGLE_SHEET_TITLE=00  # название вашего листа в журнале
# словарь с данными от сервисного аккаунта без пробелов в одну строчку словарем
GOOGLE_APPLICATION_CREDENTIALS={"type": "service_account","project_id": "..","private_key_id": "многабукав","private_key": "-----BEGIN PRIVATE KEY---......
```
Вот такой список у вас должен получиться. ![img_1.png](_images_for_readme/img_3.png) На этом все. Если не работает, можете написать [сюда в тг](https://t.me/macarell).
## Как получить некоторые поля?
<code>GOOGLE_APPLICATION_CREDENTIALS</code>
: Давайте разберемся с аккаунтом гугл, который будет автоматически редактировать гугл табличку. Я использую фреймворк gspread для взаимодействия с табличками, а он просит от нас сервисного аккаунта. Как его создать, [читайте тут](https://habr.com/ru/articles/825404/). Последним выполненным шагом в этой статье должен быть <mark>Активируем Google Sheets API</mark>. 
В переменную <code>GOOGLE_APPLICATION_CREDENTIALS</code> необходимо записать именно содержимое .json файла Вашего ключа. 
Email аккаунта нужно сохранить и попросить старшего куратора разрешить ему доступ на редактирование таблички :(

<code>GOOGLE_TABLE_ID</code>
: Возьмите ссылку на журнал `https://docs.google.com/spreadsheets/d/`<mark>здесь_айдишник</mark>`/edit?pli=1&gid=00#gid=00`.

<code>VK_API_TOKEN</code>
: Заходим в настройки группы Вконтакте. Выбираем Работа с API. Создаем ключ, даем ему всевозможные права (это важно). Копируем сам ключ и вставляем в поле.  ![img.png](_images_for_readme/img_4.png)

<code>VK_GROUP_ID</code>
: Возьмите ссылку на главную страницу вашего сообщества `https://vk.com/club000000000`. Цифры после слова club - айди вашей группы.

<code>MODULE_ID</code>
: Зайдите на сайт с журналом. Выберите предмет, курс, блок. Нажмите "Найти". Далее скопируйте ссылку и возьмите поле module_id из ссылки.
`https://api.домен.ru/что-то_написано/index?какие-то_параметры&module_id=0000&...`