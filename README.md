# Курсовой проект по ООП “Парсер вакансий”
## Описание
Проект представляет собой программу-бота в ВКонтакте, которая предоставляет сервис знакомств.  
Кандидатуры для знакомства подбираются так же из пользователей ВК со статусом "В активном поиске".  
Реализовано взаимодействие с **API ВКонтакте**, по мере работы с посетителями информация сохраняется в БД **Postgress**.  

Реализована возможность поиска кандидатур для знакомства по полу, возрасту, городу проживания.
Так же реализовано добавление понравившихся кандидатур в папку "Избранное".
Непонравившихся можно добавлять в "Чёрный список".
Позднее эти списки можно просматривать и редактировать.  

## Интерфейс
Для пользования сервисом нужно зайти в определённую [группу ВК](https://vk.com/club220121295) и нажать кнопку:

![pic](pics/pic01.PNG)

Для начала общения нужно написать боту "Старт"

После этого на экране возникнет кнопочное меню с возможными действиями пользователя:

![pic](pics/pic02.PNG)
