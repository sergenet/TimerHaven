#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_weather.py

Generates localized static HTML pages for the "Weather" tool in 7 languages:
 - Main Tool Pages:      weather-xx.html
 - How-to Article Pages: weather-how-to-xx.html
 - Tips Article Pages:   weather-tips-xx.html
 - A redirect landing page: weather.html (in output folder)

Output folder (default): ./weather_pages

Features:
 - Localized UI strings for en, fr, es, de, ru, el, ar
 - Localized city lists per language (option value = canonical city name, label = localized)
 - Localized "Powered by" line with provider link preserved
 - Removes the visible middle-card main title on the page (keeps page <title> for SEO)
 - Adds CSS to prevent link underlines inside .article-card lists and keeps them non-underlined on hover
 - Arabic pages include dir="rtl"

Usage:
  python generate_weather.py
  python generate_weather.py --root   # also write weather.html into current dir
"""
from __future__ import annotations
import os
import sys
import html
from typing import Dict, List

OUTPUT_DIR = "weather_pages"
DEFAULT_COPYRIGHT = "&copy; 2025 TimerHaven."

TRANSLATIONS: Dict[str, Dict] = {
    "en": {
        "lang_name": "English",
        "ui": {
            "select_prompt": "Select city...",
            "input_placeholder": "Or enter city...",
            "get_btn": "Get Weather",
            "use_location_btn": "Use My Location",
            "please_select": "Please select or enter a city.",
            "geolocation_unsupported": "Geolocation not supported.",
            "unable_location": "Unable to get your location.",
            "fetch_error": "Error fetching weather data.",
            "not_found": "Could not find weather for \"{city}\".",
            "back_main": "Back to Main Menu"
        },
        "main": {
            "title": "Global Weather — TimerHaven",
            "desc": "Check weather for cities worldwide instantly.",
            "howto_link": "weather-how-to-en.html",
            "howto_btn": "Read Full Article",
            "tips_link": "weather-tips-en.html",
            "tips_btn": "Read Full Article",
            "powered_by": 'Powered by <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a>',
            "cities": [
                {"value": "New York", "label": "New York"},
                {"value": "London", "label": "London"},
                {"value": "Paris", "label": "Paris"},
                {"value": "Berlin", "label": "Berlin"},
                {"value": "Tokyo", "label": "Tokyo"},
                {"value": "Sydney", "label": "Sydney"},
                {"value": "São Paulo", "label": "São Paulo"},
                {"value": "Moscow", "label": "Moscow"},
                {"value": "Dubai", "label": "Dubai"},
                {"value": "Istanbul", "label": "Istanbul"},
                {"value": "Johannesburg", "label": "Johannesburg"},
                {"value": "Toronto", "label": "Toronto"},
                {"value": "Mexico City", "label": "Mexico City"},
                {"value": "Los Angeles", "label": "Los Angeles"},
                {"value": "Mumbai", "label": "Mumbai"},
                {"value": "Cairo", "label": "Cairo"},
                {"value": "Singapore", "label": "Singapore"},
                {"value": "Hong Kong", "label": "Hong Kong"},
                {"value": "Bangkok", "label": "Bangkok"},
                {"value": "Seoul", "label": "Seoul"},
                {"value": "San Francisco", "label": "San Francisco"},
                {"value": "Rome", "label": "Rome"},
                {"value": "Kolkata", "label": "Kolkata"},
                {"value": "Jakarta", "label": "Jakarta"},
                {"value": "Madrid", "label": "Madrid"},
                {"value": "Cape Town", "label": "Cape Town"},
                {"value": "Lagos", "label": "Lagos"},
                {"value": "Melbourne", "label": "Melbourne"},
                {"value": "Beijing", "label": "Beijing"},
                {"value": "Chicago", "label": "Chicago"},
                {"value": "Vancouver", "label": "Vancouver"},
                {"value": "Auckland", "label": "Auckland"},
                {"value": "Hanoi", "label": "Hanoi"},
                {"value": "Manila", "label": "Manila"},
                {"value": "Warsaw", "label": "Warsaw"}
            ],
            "faq_items": [
                "<b>How accurate is the weather?</b> Data is provided by Open-Meteo or similar APIs.",
                "<b>Can I use my location?</b> Yes, click <b>Use My Location</b> to get local weather.",
                "<b>Can I enter any city?</b> Yes! Type any city in the input box."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Privacy Policy</a> &bull; <a href="terms.html">Terms</a> &bull; <a href="contact.html">Contact</a>'
        },
        "howto": {
            "title": "How to Use Weather",
            "steps_title": "How to use",
            "desc": "The <strong>Weather</strong> tool gives you instant forecasts for any location. Here’s how to use it:",
            "steps": [
                "<b>Select or enter a city:</b> Choose from the dropdown or type your own.",
                "<b>Use location:</b> Click the <strong>Use My Location</strong> button to use your device’s location.",
                "<b>View results:</b> Click <strong>Get Weather</strong> to see current weather info."
            ],
            "back_btn": "Back to Weather",
            "back_link": "weather-en.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Weather Tips",
            "tips_title": "Top Tips",
            "desc": "Make checking the weather easier with these tips:",
            "tips": [
                "<b>Plan ahead:</b> Check the weather before traveling or events.",
                "<b>Use location:</b> Get instant local weather updates.",
                "<b>Save time:</b> Use the dropdown for popular cities."
            ],
            "back_btn": "Back to Weather",
            "back_link": "weather-en.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "fr": {
        "lang_name": "Français",
        "ui": {
            "select_prompt": "Sélectionnez une ville...",
            "input_placeholder": "Ou saisissez la ville...",
            "get_btn": "Obtenir la météo",
            "use_location_btn": "Utiliser ma position",
            "please_select": "Veuillez sélectionner ou saisir une ville.",
            "geolocation_unsupported": "Géolocalisation non prise en charge.",
            "unable_location": "Impossible d'obtenir votre position.",
            "fetch_error": "Erreur lors de la récupération des données météo.",
            "not_found": "Météo introuvable pour «{city}».",
            "back_main": "Retour au menu principal"
        },
        "main": {
            "title": "Météo mondiale — TimerHaven",
            "desc": "Consultez la météo des villes du monde en un instant.",
            "howto_link": "weather-how-to-fr.html",
            "howto_btn": "Lire l'article",
            "tips_link": "weather-tips-fr.html",
            "tips_btn": "Lire l'article",
            "powered_by": 'Données par <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a>',
            "cities": [
                {"value": "New York", "label": "New York"},
                {"value": "London", "label": "Londres"},
                {"value": "Paris", "label": "Paris"},
                {"value": "Berlin", "label": "Berlin"},
                {"value": "Tokyo", "label": "Tokyo"},
                {"value": "Sydney", "label": "Sydney"},
                {"value": "São Paulo", "label": "São Paulo"},
                {"value": "Moscow", "label": "Moscou"},
                {"value": "Dubai", "label": "Dubaï"},
                {"value": "Istanbul", "label": "Istanbul"},
                {"value": "Johannesburg", "label": "Johannesburg"},
                {"value": "Toronto", "label": "Toronto"},
                {"value": "Mexico City", "label": "Mexico"},
                {"value": "Los Angeles", "label": "Los Angeles"},
                {"value": "Mumbai", "label": "Mumbai"},
                {"value": "Cairo", "label": "Le Caire"},
                {"value": "Singapore", "label": "Singapour"},
                {"value": "Hong Kong", "label": "Hong Kong"},
                {"value": "Bangkok", "label": "Bangkok"},
                {"value": "Seoul", "label": "Séoul"},
                {"value": "San Francisco", "label": "San Francisco"},
                {"value": "Rome", "label": "Rome"},
                {"value": "Kolkata", "label": "Kolkata"},
                {"value": "Jakarta", "label": "Jakarta"},
                {"value": "Madrid", "label": "Madrid"},
                {"value": "Cape Town", "label": "Le Cap"},
                {"value": "Lagos", "label": "Lagos"},
                {"value": "Melbourne", "label": "Melbourne"},
                {"value": "Beijing", "label": "Pékin"},
                {"value": "Chicago", "label": "Chicago"},
                {"value": "Vancouver", "label": "Vancouver"},
                {"value": "Auckland", "label": "Auckland"},
                {"value": "Hanoi", "label": "Hanoï"},
                {"value": "Manila", "label": "Manille"},
                {"value": "Warsaw", "label": "Varsovie"}
            ],
            "faq_items": [
                "<b>Quelle est la précision ?</b> Les données proviennent d'APIs comme Open-Meteo.",
                "<b>Puis-je utiliser ma position ?</b> Oui, cliquez sur <b>Utiliser ma position</b>.",
                "<b>Puis-je saisir n'importe quelle ville ?</b> Oui ! Tapez la ville dans le champ."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Politique</a>'
        },
        "howto": {
            "title": "Comment utiliser la météo",
            "steps_title": "Comment utiliser",
            "desc": "L'outil <strong>Météo</strong> vous donne des prévisions instantanées. Voici comment l'utiliser :",
            "steps": [
                "<b>Sélectionnez ou saisissez une ville :</b> Choisissez dans la liste ou tapez la vôtre.",
                "<b>Utilisez la position :</b> Cliquez sur <strong>Utiliser ma position</strong> pour utiliser la localisation de l'appareil.",
                "<b>Voir les résultats :</b> Cliquez sur <strong>Obtenir la météo</strong> pour voir l'état actuel."
            ],
            "back_btn": "Retour à la météo",
            "back_link": "weather-fr.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Conseils Météo",
            "tips_title": "Conseils",
            "desc": "Facilitez-vous la météo avec ces conseils :",
            "tips": [
                "<b>Planifiez :</b> Vérifiez la météo avant un voyage ou un événement.",
                "<b>Utilisez la position :</b> Obtenez la météo locale instantanément.",
                "<b>Gagnez du temps :</b> Utilisez la liste pour les villes populaires."
            ],
            "back_btn": "Retour à la météo",
            "back_link": "weather-fr.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "es": {
        "lang_name": "Español",
        "ui": {
            "select_prompt": "Seleccione ciudad...",
            "input_placeholder": "O introduzca la ciudad...",
            "get_btn": "Obtener clima",
            "use_location_btn": "Usar mi ubicación",
            "please_select": "Por favor seleccione o escriba una ciudad.",
            "geolocation_unsupported": "Geolocalización no soportada.",
            "unable_location": "No se pudo obtener su ubicación.",
            "fetch_error": "Error al obtener datos meteorológicos.",
            "not_found": "No se encontró el clima para \"{city}\".",
            "back_main": "Volver al menú principal"
        },
        "main": {
            "title": "Clima Global — TimerHaven",
            "desc": "Consulta el clima de ciudades del mundo al instante.",
            "howto_link": "weather-how-to-es.html",
            "howto_btn": "Leer el artículo",
            "tips_link": "weather-tips-es.html",
            "tips_btn": "Leer el artículo",
            "powered_by": 'Datos de <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a>',
            "cities": [
                {"value": "New York", "label": "Nueva York"},
                {"value": "London", "label": "Londres"},
                {"value": "Paris", "label": "París"},
                {"value": "Berlin", "label": "Berlín"},
                {"value": "Tokyo", "label": "Tokio"},
                {"value": "Sydney", "label": "Sídney"},
                {"value": "São Paulo", "label": "São Paulo"},
                {"value": "Moscow", "label": "Moscú"},
                {"value": "Dubai", "label": "Dubái"},
                {"value": "Istanbul", "label": "Estambul"},
                {"value": "Johannesburg", "label": "Johannesburgo"},
                {"value": "Toronto", "label": "Toronto"},
                {"value": "Mexico City", "label": "Ciudad de México"},
                {"value": "Los Angeles", "label": "Los Ángeles"},
                {"value": "Mumbai", "label": "Mumbai"},
                {"value": "Cairo", "label": "El Cairo"},
                {"value": "Singapore", "label": "Singapur"},
                {"value": "Hong Kong", "label": "Hong Kong"},
                {"value": "Bangkok", "label": "Bangkok"},
                {"value": "Seoul", "label": "Seúl"},
                {"value": "San Francisco", "label": "San Francisco"},
                {"value": "Rome", "label": "Roma"},
                {"value": "Kolkata", "label": "Kolkata"},
                {"value": "Jakarta", "label": "Yakarta"},
                {"value": "Madrid", "label": "Madrid"},
                {"value": "Cape Town", "label": "Ciudad del Cabo"},
                {"value": "Lagos", "label": "Lagos"},
                {"value": "Melbourne", "label": "Melbourne"},
                {"value": "Beijing", "label": "Pekín"},
                {"value": "Chicago", "label": "Chicago"},
                {"value": "Vancouver", "label": "Vancouver"},
                {"value": "Auckland", "label": "Auckland"},
                {"value": "Hanoi", "label": "Hanói"},
                {"value": "Manila", "label": "Manila"},
                {"value": "Warsaw", "label": "Varsovia"}
            ],
            "faq_items": [
                "<b>¿Qué tan precisa es la información?</b> Los datos provienen de APIs como Open-Meteo.",
                "<b>¿Puedo usar mi ubicación?</b> Sí, haga clic en <b>Usar mi ubicación</b>.",
                "<b>¿Puedo escribir cualquier ciudad?</b> ¡Sí! Escriba la ciudad en el campo."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Política</a>'
        },
        "howto": {
            "title": "Cómo usar el clima",
            "steps_title": "Cómo usar",
            "desc": "La herramienta de <strong>Clima</strong> ofrece previsiones instantáneas. Así es como se usa:",
            "steps": [
                "<b>Seleccione o escriba una ciudad:</b> Elija del desplegable o escriba la suya.",
                "<b>Use la ubicación:</b> Haga clic en <strong>Usar mi ubicación</strong>.",
                "<b>Ver resultados:</b> Haga clic en <strong>Obtener clima</strong> para ver el estado actual."
            ],
            "back_btn": "Volver al clima",
            "back_link": "weather-es.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Consejos del clima",
            "tips_title": "Consejos principales",
            "desc": "Haz el chequeo del clima más fácil con estos consejos:",
            "tips": [
                "<b>Planifica:</b> Revisa el clima antes de viajar o eventos.",
                "<b>Usa la ubicación:</b> Obtén el clima local al instante.",
                "<b>Ahorra tiempo:</b> Usa la lista para ciudades populares."
            ],
            "back_btn": "Volver al clima",
            "back_link": "weather-es.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "de": {
        "lang_name": "Deutsch",
        "ui": {
            "select_prompt": "Stadt auswählen...",
            "input_placeholder": "Oder Stadt eingeben...",
            "get_btn": "Wetter abrufen",
            "use_location_btn": "Meine Position verwenden",
            "please_select": "Bitte wählen oder geben Sie eine Stadt ein.",
            "geolocation_unsupported": "Geolocation wird nicht unterstützt.",
            "unable_location": "Standort konnte nicht ermittelt werden.",
            "fetch_error": "Fehler beim Abrufen der Wetterdaten.",
            "not_found": "Für \"{city}\" konnte kein Wetter gefunden werden.",
            "back_main": "Zurück zum Hauptmenü"
        },
        "main": {
            "title": "Weltwetter — TimerHaven",
            "desc": "Prüfen Sie das Wetter weltweit sofort.",
            "howto_link": "weather-how-to-de.html",
            "howto_btn": "Artikel lesen",
            "tips_link": "weather-tips-de.html",
            "tips_btn": "Artikel lesen",
            "powered_by": 'Daten von <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a>',
            "cities": [
                {"value": "New York", "label": "New York"},
                {"value": "London", "label": "London"},
                {"value": "Paris", "label": "Paris"},
                {"value": "Berlin", "label": "Berlin"},
                {"value": "Tokyo", "label": "Tokio"},
                {"value": "Sydney", "label": "Sydney"},
                {"value": "São Paulo", "label": "São Paulo"},
                {"value": "Moscow", "label": "Moskau"},
                {"value": "Dubai", "label": "Dubai"},
                {"value": "Istanbul", "label": "Istanbul"},
                {"value": "Johannesburg", "label": "Johannesburg"},
                {"value": "Toronto", "label": "Toronto"},
                {"value": "Mexico City", "label": "Mexiko-Stadt"},
                {"value": "Los Angeles", "label": "Los Angeles"},
                {"value": "Mumbai", "label": "Mumbai"},
                {"value": "Cairo", "label": "Kairo"},
                {"value": "Singapore", "label": "Singapur"},
                {"value": "Hong Kong", "label": "Hongkong"},
                {"value": "Bangkok", "label": "Bangkok"},
                {"value": "Seoul", "label": "Seoul"},
                {"value": "San Francisco", "label": "San Francisco"},
                {"value": "Rome", "label": "Rom"},
                {"value": "Kolkata", "label": "Kolkata"},
                {"value": "Jakarta", "label": "Jakarta"},
                {"value": "Madrid", "label": "Madrid"},
                {"value": "Cape Town", "label": "Kapstadt"},
                {"value": "Lagos", "label": "Lagos"},
                {"value": "Melbourne", "label": "Melbourne"},
                {"value": "Beijing", "label": "Peking"},
                {"value": "Chicago", "label": "Chicago"},
                {"value": "Vancouver", "label": "Vancouver"},
                {"value": "Auckland", "label": "Auckland"},
                {"value": "Hanoi", "label": "Hanoi"},
                {"value": "Manila", "label": "Manila"},
                {"value": "Warsaw", "label": "Warschau"}
            ],
            "faq_items": [
                "<b>Wie genau ist das Wetter?</b> Daten stammen von Open-Meteo oder ähnlichen APIs.",
                "<b>Kann ich meinen Standort verwenden?</b> Ja, klicken Sie auf <b>Meine Position verwenden</b>.",
                "<b>Kann ich jede Stadt eingeben?</b> Ja! Geben Sie die Stadt in das Feld ein."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Datenschutz</a>'
        },
        "howto": {
            "title": "So verwenden Sie das Wetter",
            "steps_title": "So verwenden",
            "desc": "Das <strong>Wetter</strong>-Tool liefert sofortige Vorhersagen. So verwenden Sie es:",
            "steps": [
                "<b>Stadt wählen oder eingeben:</b> Wählen Sie aus der Liste oder geben Sie Ihre eigene Stadt ein.",
                "<b>Standort verwenden:</b> Klicken Sie auf <strong>Meine Position verwenden</strong>.",
                "<b>Ergebnisse anzeigen:</b> Klicken Sie auf <strong>Wetter abrufen</strong>."
            ],
            "back_btn": "Zurück zum Wetter",
            "back_link": "weather-de.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Wettertipps",
            "tips_title": "Top-Tipps",
            "desc": "Machen Sie die Wetterprüfung einfacher mit diesen Tipps:",
            "tips": [
                "<b>Planen Sie voraus:</b> Prüfen Sie das Wetter vor Reisen oder Veranstaltungen.",
                "<b>Standort verwenden:</b> Holen Sie sich lokale Updates sofort.",
                "<b>Zeit sparen:</b> Verwenden Sie das Dropdown für beliebte Städte."
            ],
            "back_btn": "Zurück zum Wetter",
            "back_link": "weather-de.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ru": {
        "lang_name": "Русский",
        "ui": {
            "select_prompt": "Выберите город...",
            "input_placeholder": "Или введите город...",
            "get_btn": "Получить погоду",
            "use_location_btn": "Использовать мое местоположение",
            "please_select": "Пожалуйста, выберите или введите город.",
            "geolocation_unsupported": "Геолокация не поддерживается.",
            "unable_location": "Не удалось получить ваше местоположение.",
            "fetch_error": "Ошибка получения погодных данных.",
            "not_found": "Не удалось найти погоду для \"{city}\".",
            "back_main": "Назад в главное меню"
        },
        "main": {
            "title": "Погода по миру — TimerHaven",
            "desc": "Проверяйте погоду для городов по всему миру мгновенно.",
            "howto_link": "weather-how-to-ru.html",
            "howto_btn": "Читать статью",
            "tips_link": "weather-tips-ru.html",
            "tips_btn": "Читать статью",
            "powered_by": 'Данные от <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a>',
            "cities": [
                {"value": "New York", "label": "Нью-Йорк"},
                {"value": "London", "label": "Лондон"},
                {"value": "Paris", "label": "Париж"},
                {"value": "Berlin", "label": "Берлин"},
                {"value": "Tokyo", "label": "Токио"},
                {"value": "Sydney", "label": "Сидней"},
                {"value": "São Paulo", "label": "Сан-Паулу"},
                {"value": "Moscow", "label": "Москва"},
                {"value": "Dubai", "label": "Дубай"},
                {"value": "Istanbul", "label": "Стамбул"},
                {"value": "Johannesburg", "label": "Йоханнесбург"},
                {"value": "Toronto", "label": "Торонто"},
                {"value": "Mexico City", "label": "Мехико"},
                {"value": "Los Angeles", "label": "Лос-Анджелес"},
                {"value": "Mumbai", "label": "Мумбаи"},
                {"value": "Cairo", "label": "Каир"},
                {"value": "Singapore", "label": "Сингапур"},
                {"value": "Hong Kong", "label": "Гонконг"},
                {"value": "Bangkok", "label": "Бангкок"},
                {"value": "Seoul", "label": "Сеул"},
                {"value": "San Francisco", "label": "Сан-Франциско"},
                {"value": "Rome", "label": "Рим"},
                {"value": "Kolkata", "label": "Калькутта"},
                {"value": "Jakarta", "label": "Джакарта"},
                {"value": "Madrid", "label": "Мадрид"},
                {"value": "Cape Town", "label": "Кейптаун"},
                {"value": "Lagos", "label": "Лагос"},
                {"value": "Melbourne", "label": "Мельбурн"},
                {"value": "Beijing", "label": "Пекин"},
                {"value": "Chicago", "label": "Чикаго"},
                {"value": "Vancouver", "label": "Ванкувер"},
                {"value": "Auckland", "label": "Окленд"},
                {"value": "Hanoi", "label": "Ханой"},
                {"value": "Manila", "label": "Манила"},
                {"value": "Warsaw", "label": "Варшава"}
            ],
            "faq_items": [
                "<b>Насколько точна погода?</b> Данные предоставляются Open-Meteo или подобными API.",
                "<b>Могу ли я использовать местоположение?</b> Да, нажмите <b>Использовать мое местоположение</b>.",
                "<b>Могу ли я ввести любой город?</b> Да! Введите город в поле."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Политика</a>'
        },
        "howto": {
            "title": "Как пользоваться погодой",
            "steps_title": "Как использовать",
            "desc": "Инструмент <strong>Погода</strong> предоставляет прогнозы моментально. Как им пользоваться:",
            "steps": [
                "<b>Выберите или введите город:</b> Выберите из выпадающего списка или введите свой.",
                "<b>Используйте местоположение:</b> Нажмите <strong>Использовать мое местоположение</strong>.",
                "<b>Просмотр результатов:</b> Нажмите <strong>Получить погоду</strong>."
            ],
            "back_btn": "Вернуться к погоде",
            "back_link": "weather-ru.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Советы по погоде",
            "tips_title": "Лучшие советы",
            "desc": "Упростите проверку погоды с этими советами:",
            "tips": [
                "<b>Планируйте заранее:</b> Проверяйте погоду перед поездками или мероприятиями.",
                "<b>Используйте местоположение:</b> Получайте локальные обновления.",
                "<b>Экономьте время:</b> Используйте список популярных городов."
            ],
            "back_btn": "Вернуться к погоде",
            "back_link": "weather-ru.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "el": {
        "lang_name": "Ελληνικά",
        "ui": {
            "select_prompt": "Επιλέξτε πόλη...",
            "input_placeholder": "Ή πληκτρολογήστε πόλη...",
            "get_btn": "Λήψη καιρού",
            "use_location_btn": "Χρήση τοποθεσίας",
            "please_select": "Επιλέξτε ή εισάγετε μια πόλη, παρακαλώ.",
            "geolocation_unsupported": "Η γεωτοποθεσία δεν υποστηρίζεται.",
            "unable_location": "Δεν μπορεί να ληφθεί η τοποθεσία σας.",
            "fetch_error": "Σφάλμα ανάκτησης δεδομένων καιρού.",
            "not_found": "Δεν βρέθηκε καιρός για «{city}».",
            "back_main": "Επιστροφή στο κύριο μενού"
        },
        "main": {
            "title": "Καιρός παγκοσμίως — TimerHaven",
            "desc": "Ελέγξτε τον καιρό για πόλεις σε όλο τον κόσμο άμεσα.",
            "howto_link": "weather-how-to-el.html",
            "howto_btn": "Διαβάστε το άρθρο",
            "tips_link": "weather-tips-el.html",
            "tips_btn": "Διαβάστε το άρθρο",
            "powered_by": 'Προμηθευτής <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a>',
            "cities": [
                {"value": "New York", "label": "Νέα Υόρκη"},
                {"value": "London", "label": "Λονδίνο"},
                {"value": "Paris", "label": "Παρίσι"},
                {"value": "Berlin", "label": "Βερολίνο"},
                {"value": "Tokyo", "label": "Τόκιο"},
                {"value": "Sydney", "label": "Σίδνεϊ"},
                {"value": "São Paulo", "label": "Σάο Πάολο"},
                {"value": "Moscow", "label": "Μόσχα"},
                {"value": "Dubai", "label": "Ντουμπάι"},
                {"value": "Istanbul", "label": "Κωνσταντινούπολη"},
                {"value": "Johannesburg", "label": "Γιοχάνεσμπουργκ"},
                {"value": "Toronto", "label": "Τόροντο"},
                {"value": "Mexico City", "label": "Πόλη του Μεξικού"},
                {"value": "Los Angeles", "label": "Λος Άντζελες"},
                {"value": "Mumbai", "label": "Μουμπάι"},
                {"value": "Cairo", "label": "Κάιρο"},
                {"value": "Singapore", "label": "Σιγκαπούρη"},
                {"value": "Hong Kong", "label": "Χονγκ Κονγκ"},
                {"value": "Bangkok", "label": "Μπανγκόκ"},
                {"value": "Seoul", "label": "Σεούλ"},
                {"value": "San Francisco", "label": "Σαν Φρανσίσκο"},
                {"value": "Rome", "label": "Ρώμη"},
                {"value": "Kolkata", "label": "Κολκάτα"},
                {"value": "Jakarta", "label": "Τζακάρτα"},
                {"value": "Madrid", "label": "Μαδρίτη"},
                {"value": "Cape Town", "label": "Κέιπ Τάουν"},
                {"value": "Lagos", "label": "Λάγος"},
                {"value": "Melbourne", "label": "Μελβούρνη"},
                {"value": "Beijing", "label": "Πεκίνο"},
                {"value": "Chicago", "label": "Σικάγο"},
                {"value": "Vancouver", "label": "Βανκούβερ"},
                {"value": "Auckland", "label": "Όκλαντ"},
                {"value": "Hanoi", "label": "Χανόι"},
                {"value": "Manila", "label": "Μανίλα"},
                {"value": "Warsaw", "label": "Βαρσοβία"}
            ],
            "faq_items": [
                "<b>Πόσο ακριβής είναι ο καιρός;</b> Τα δεδομένα παρέχονται από Open-Meteo ή παρόμοια APIs.",
                "<b>Μπορώ να χρησιμοποιήσω την τοποθεσία μου;</b> Ναι, πατήστε <b>Χρήση τοποθεσίας</b>.",
                "<b>Μπορώ να εισάγω οποιαδήποτε πόλη;</b> Ναι! Πληκτρολογήστε την πόλη."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">Πολιτική</a>'
        },
        "howto": {
            "title": "Πώς να χρησιμοποιήσετε τον καιρό",
            "steps_title": "Πώς να χρησιμοποιήσετε",
            "desc": "Το εργαλείο <strong>Καιρός</strong> δίνει άμεσα προβλέψεις. Πώς να το χρησιμοποιήσετε:",
            "steps": [
                "<b>Επιλέξτε ή εισάγετε πόλη:</b> Επιλέξτε από τη λίστα ή πληκτρολογήστε τη δική σας.",
                "<b>Χρήση τοποθεσίας:</b> Πατήστε <strong>Χρήση τοποθεσίας</strong>.",
                "<b>Δείτε τα αποτελέσματα:</b> Πατήστε <strong>Λήψη καιρού</strong>."
            ],
            "back_btn": "Επιστροφή στον καιρό",
            "back_link": "weather-el.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "Συμβουλές Καιρού",
            "tips_title": "Κορυφαίες συμβουλές",
            "desc": "Κάντε τον έλεγχο καιρού ευκολότερο με αυτές τις συμβουλές:",
            "tips": [
                "<b>Σχεδιάστε εκ των προτέρων:</b> Ελέγξτε τον καιρό πριν ταξίδια ή εκδηλώσεις.",
                "<b>Χρησιμοποιήστε τοποθεσία:</b> Λάβετε τοπικές ενημερώσεις άμεσα.",
                "<b>Εξοικονομήστε χρόνο:</b> Χρησιμοποιήστε τη λίστα για δημοφιλείς πόλεις."
            ],
            "back_btn": "Επιστροφή στον καιρό",
            "back_link": "weather-el.html",
            "footer": DEFAULT_COPYRIGHT
        }
    },

    "ar": {
        "lang_name": "العربية",
        "ui": {
            "select_prompt": "اختر مدينة...",
            "input_placeholder": "أو ادخل المدينة...",
            "get_btn": "الحصول على الطقس",
            "use_location_btn": "استخدام موقعي",
            "please_select": "يرجى اختيار مدينة أو إدخالها.",
            "geolocation_unsupported": "الموقع الجغرافي غير مدعوم.",
            "unable_location": "تعذر الحصول على موقعك.",
            "fetch_error": "خطأ في جلب بيانات الطقس.",
            "not_found": "تعذر العثور على الطقس لـ \"{city}\".",
            "back_main": "العودة إلى القائمة الرئيسية"
        },
        "main": {
            "title": "الطقس العالمي — TimerHaven",
            "desc": "تحقق من الطقس للمدن حول العالم فورًا.",
            "howto_link": "weather-how-to-ar.html",
            "howto_btn": "اقرأ المقالة",
            "tips_link": "weather-tips-ar.html",
            "tips_btn": "اقرأ المقالة",
            "powered_by": 'مقدم البيانات <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a>',
            "cities": [
                {"value": "New York", "label": "نيويورك"},
                {"value": "London", "label": "لندن"},
                {"value": "Paris", "label": "باريس"},
                {"value": "Berlin", "label": "برلين"},
                {"value": "Tokyo", "label": "طوكيو"},
                {"value": "Sydney", "label": "سيدني"},
                {"value": "São Paulo", "label": "ساو باولو"},
                {"value": "Moscow", "label": "موسكو"},
                {"value": "Dubai", "label": "دبي"},
                {"value": "Istanbul", "label": "اسطنبول"},
                {"value": "Johannesburg", "label": "جوهانسبرج"},
                {"value": "Toronto", "label": "تورونتو"},
                {"value": "Mexico City", "label": "مكسيكو سيتي"},
                {"value": "Los Angeles", "label": "لوس أنجلوس"},
                {"value": "Mumbai", "label": "مومباي"},
                {"value": "Cairo", "label": "القاهرة"},
                {"value": "Singapore", "label": "سنغافورة"},
                {"value": "Hong Kong", "label": "هونغ كونغ"},
                {"value": "Bangkok", "label": "بانكوك"},
                {"value": "Seoul", "label": "سيول"},
                {"value": "San Francisco", "label": "سان فرانسيسكو"},
                {"value": "Rome", "label": "روما"},
                {"value": "Kolkata", "label": "كولكاتا"},
                {"value": "Jakarta", "label": "جاكرتا"},
                {"value": "Madrid", "label": "مدريد"},
                {"value": "Cape Town", "label": "كيب تاون"},
                {"value": "Lagos", "label": "لاجوس"},
                {"value": "Melbourne", "label": "ملبورن"},
                {"value": "Beijing", "label": "بكين"},
                {"value": "Chicago", "label": "شيكاغو"},
                {"value": "Vancouver", "label": "فانكوفر"},
                {"value": "Auckland", "label": "أوكلاند"},
                {"value": "Hanoi", "label": "هانوي"},
                {"value": "Manila", "label": "مانيلا"},
                {"value": "Warsaw", "label": "وارسو"}
            ],
            "faq_items": [
                "<b>ما مدى دقة الطقس؟</b> البيانات مقدمة من Open-Meteo أو APIs مماثلة.",
                "<b>هل يمكنني استخدام موقعي؟</b> نعم، انقر على <b>استخدام موقعي</b>.",
                "<b>هل يمكنني إدخال أي مدينة؟</b> نعم! اكتب المدينة في الحقل."
            ],
            "footer": DEFAULT_COPYRIGHT + ' <a href="privacy.html">سياسة الخصوصية</a>'
        },
        "howto": {
            "title": "كيفية استخدام الطقس",
            "steps_title": "كيفية الاستخدام",
            "desc": "أداة <strong>الطقس</strong> تمنحك توقعات فورية لأي موقع. كيفية الاستخدام:",
            "steps": [
                "<b>اختر أو ادخل مدينة:</b> اختر من القائمة أو اكتب مدينتك.",
                "<b>استخدم الموقع:</b> اضغط <strong>استخدام موقعي</strong>.",
                "<b>عرض النتائج:</b> اضغط <strong>الحصول على الطقس</strong>."
            ],
            "back_btn": "العودة إلى الطقس",
            "back_link": "weather-ar.html",
            "footer": DEFAULT_COPYRIGHT
        },
        "tips": {
            "title": "نصائح الطقس",
            "tips_title": "أهم النصائح",
            "desc": "اجعل فحص الطقس أسهل بهذه النصائح:",
            "tips": [
                "<b>خطط مسبقًا:</b> افحص الطقس قبل السفر أو الأحداث.",
                "<b>استخدم الموقع:</b> احصل على تحديثات محلية فورية.",
                "<b>وفر وقتًا:</b> استخدم القائمة للمدن الشائعة."
            ],
            "back_btn": "العودة إلى الطقس",
            "back_link": "weather-ar.html",
            "footer": DEFAULT_COPYRIGHT
        }
    }
}

ALLOWED_INLINE_TAGS = {"b", "strong", "a", "br"}


def escape_allow_tags(s: str) -> str:
    if not isinstance(s, str):
        return ""
    esc = html.escape(s, quote=True)
    for tag in ALLOWED_INLINE_TAGS:
        esc = esc.replace(html.escape(f"<{tag}>"), f"<{tag}>")
        esc = esc.replace(html.escape(f"</{tag}>"), f"</{tag}>")
        esc = esc.replace(html.escape(f"<{tag} "), f"<{tag} ")
    return esc


def js_string_literal(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def build_city_options_html(cities: List[Dict[str, str]], select_prompt: str) -> str:
    html_parts = [f'<option value="">{escape_allow_tags(select_prompt)}</option>']
    for c in cities:
        val = c.get("value", "")
        label = c.get("label", val)
        html_parts.append(f'<option value="{html.escape(val)}">{escape_allow_tags(label)}</option>')
    return "\n              ".join(html_parts)


def generate_main_html(code: str, data: Dict) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    ui = data.get("ui", {})
    main = data["main"]
    howto = data.get("howto", {})
    tips = data.get("tips", {})

    language_options = [
        ("en", "English"), ("fr", "Français"), ("es", "Español"),
        ("de", "Deutsch"), ("ru", "Русский"), ("el", "Ελληνικά"), ("ar", "العربية")
    ]
    options_html = "".join(
        f'<option value="{lang}"{" selected" if lang == code else ""}>{html.escape(name)}</option>'
        for lang, name in language_options
    )

    select_prompt = ui.get("select_prompt", "Select city...")
    input_placeholder = escape_allow_tags(ui.get("input_placeholder", "Or enter city..."))
    get_btn = escape_allow_tags(ui.get("get_btn", "Get Weather"))
    use_location_btn = escape_allow_tags(ui.get("use_location_btn", "Use My Location"))

    please_select_js = js_string_literal(ui.get("please_select", "Please select or enter a city."))
    geolocation_unsupported_js = js_string_literal(ui.get("geolocation_unsupported", "Geolocation not supported."))
    unable_location_js = js_string_literal(ui.get("unable_location", "Unable to get your location."))
    fetch_error_js = js_string_literal(ui.get("fetch_error", "Error fetching weather data."))
    not_found_template_js = js_string_literal(ui.get("not_found", 'Could not find weather for "{city}".'))

    faq_html = "\n            ".join(f"<li>{escape_allow_tags(item)}</li>" for item in main.get("faq_items", []))

    main_title = escape_allow_tags(main.get("title", "Global Weather — TimerHaven"))
    main_desc = escape_allow_tags(main.get("desc", ""))

    howto_card_title = escape_allow_tags(howto.get("title", "How to Use Weather"))
    tips_card_title = escape_allow_tags(tips.get("title", "Weather Tips"))

    cities = main.get("cities", [])
    city_options_html = build_city_options_html(cities, select_prompt)

    powered_by_html = main.get("powered_by", 'Powered by <a href="https://open-meteo.com" target="_blank" rel="noopener">Open-Meteo</a>')
    powered_by_html = escape_allow_tags(powered_by_html)

    html_out = f"""<!doctype html>
<html lang="{code}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{main_title}</title>
  <meta name="description" content="{main_desc}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <style>
    body {{ background:#f4f7fb; font-family:'Montserrat', Arial, sans-serif; color:#0b2545; }}
    .page-wrap {{ max-width:1200px; margin:2rem auto; padding:0 1rem; }}
    .top-row {{ display:flex; justify-content:flex-end; gap:.6rem; margin-bottom:.6rem; }}
    .language-select {{ width:220px; border-radius:10px; padding:.28rem .6rem; border:1px solid rgba(13,110,253,0.25); background:#fff; color:#0d6efd; }}
    .center-row {{ display:flex; gap:1.6rem; justify-content:center; align-items:flex-start; }}
    .article-card, .tool-card {{ background:#fff; border-radius:16px; box-shadow:0 2px 12px rgba(0,0,0,0.06); padding:1.3rem; }}
    .article-card {{ width:330px; min-width:200px; min-height:340px; height:340px; display:flex; flex-direction:column; justify-content:space-between; align-items:flex-start; }}
    .tool-card {{ width:410px; min-width:240px; min-height:330px; display:flex; flex-direction:column; }}
    .article-card h2 {{ color:#185a9d; font-size:1.25rem; margin-bottom:.6rem; }}
    .tool-card h3 {{ color:#185a9d; font-size:1.35rem; margin-bottom:.5rem; }}
    .weather-form-row {{ display:flex; gap:.5rem; margin-bottom:1rem; align-items:center; flex-wrap:wrap; }}
    .weather-result {{ margin-top:1rem; background:#f7fafc; border-radius:7px; padding:1rem; font-size:1.15em; min-height:48px; }}
    .powered-by {{ margin-top:0.5rem; font-size:0.9em; color:#6b7280; }}
    .action-row {{ display:flex; gap:.7rem; flex-wrap:wrap; }}
    #getWeatherBtn {{ width:175px; height:42px; font-size:1.07em; background:#157af6; color:#fff; border:none; border-radius:8px; font-weight:600; box-shadow:0 2px 8px #e0e7ef; cursor:pointer; }}
    #useLocationBtn {{ background:#444; color:#fff; border-radius:8px; font-size:1.07em; font-weight:600; border:none; padding:0.4em 1.1em; width:175px; height:42px; display:inline-flex; align-items:center; gap:.4em; cursor:pointer; }}
    @media (max-width:750px) {{ #getWeatherBtn,#useLocationBtn{{width:100%;}} .weather-form-row{{flex-direction:column;align-items:stretch;}} .action-row{{flex-direction:column;}} }}
    footer.site {{ text-align:center; margin-top:1.5rem; color:#6b7280; }}

    /* Strong rule: remove underlines for links in article-card lists and do NOT add underline on hover */
    .article-card a,
    .article-card ul a,
    .article-card ol a,
    .article-card li a,
    .article-card ul li a,
    .article-card ol li a {{
      text-decoration: none !important;
      color: inherit !important;
    }}
    .article-card a:hover,
    .article-card ul a:hover,
    .article-card ol a:hover,
    .article-card li a:hover,
    .article-card ul li a:hover,
    .article-card ol li a:hover {{
      text-decoration: none !important;
      color: inherit !important;
    }}
  </style>
</head>
<body>
  <div class="page-wrap">
    <div class="top-row">
      <label for="language-select-top" style="align-self:center; font-weight:600; margin-right:.5rem;">Language:</label>
      <select id="language-select-top" class="language-select" aria-label="Language selector">
        {options_html}
      </select>
    </div>

    <div class="text-center mb-4">
      <h1 style="margin-bottom:.25rem;">{main_title}</h1>
      <p class="lead" style="color:#374151; margin-bottom:1rem;">{main_desc}</p>
    </div>

    <div class="center-row">
      <div class="article-card" aria-labelledby="howto-title">
        <div>
          <h2 id="howto-title"><i class="fa fa-cloud-sun"></i> {howto_card_title}</h2>
          <ol style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(s)}</li>" for s in howto.get('steps', []))}
          </ol>
        </div>
        <a href="{main.get('howto_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.6rem;">{escape_allow_tags(main.get('howto_btn'))}</a>
      </div>

      <div class="tool-card" role="region" aria-label="Global Weather">
        <a href="index.html" class="back-link">&larr; {escape_allow_tags(ui.get('back_main', main.get('back_main','Back to Main Menu')))}</a>

        <!-- Middle visible title intentionally removed to keep the card minimal per request -->

        <form id="weatherForm" autocomplete="off">
          <div class="weather-form-row">
            <select id="cityDropdown" class="form-select" title="{escape_allow_tags(select_prompt)}" style="min-width:140px;">
              {city_options_html}
            </select>
            <input type="text" id="cityInput" class="form-control" placeholder="{input_placeholder}" title="{input_placeholder}" style="min-width:160px;">
          </div>

          <div class="action-row">
            <button type="submit" id="getWeatherBtn">{get_btn}</button>
            <button type="button" id="useLocationBtn"><i class="fa fa-location-arrow"></i> {use_location_btn}</button>
          </div>
        </form>

        <div id="weatherResult" class="weather-result"></div>
        <div class="powered-by">{powered_by_html}</div>

        <details class="faq-section" style="margin-top:1rem;">
          <summary style="font-weight:700; font-size:1rem;">{escape_allow_tags(main.get('faq_title'))}</summary>
          <ul style="padding-left:1.1rem; color:#374151;">
            {faq_html}
          </ul>
        </details>
      </div>

      <div class="article-card" aria-labelledby="tips-title">
        <div>
          <h2 id="tips-title"><i class="fa fa-lightbulb" style="color:#43cea2;"></i> {tips_card_title}</h2>
          <ul style="padding-left:1.1rem; color:#374151;">
            {"".join(f"<li>{escape_allow_tags(t)}</li>" for t in tips.get('tips', []))}
          </ul>
        </div>
        <a href="{main.get('tips_link')}" class="btn btn-outline-primary btn-sm" style="align-self:stretch; margin-top:.6rem;">{escape_allow_tags(main.get('tips_btn'))}</a>
      </div>
    </div>

    <footer class="site">
      {main.get('footer')}
    </footer>
  </div>

  <script>
  // localized JS strings
  const MSG_PLEASE_SELECT = "{please_select_js}";
  const MSG_GEO_UNSUPPORTED = "{geolocation_unsupported_js}";
  const MSG_UNABLE_LOCATION = "{unable_location_js}";
  const MSG_FETCH_ERROR = "{fetch_error_js}";
  const MSG_NOT_FOUND_TEMPLATE = "{not_found_template_js}";

  function renderWeatherData(data) {{
    return `<b>${{data.name}}, ${{data.sys.country}}</b><br>
            Weather: ${{data.weather[0].description}}<br>
            Temperature: ${{data.main.temp}}&deg;C<br>
            Humidity: ${{data.main.humidity}}%<br>
            Wind: ${{data.wind.speed}} m/s`;
  }}

  function fetchWeather(city) {{
    const resultEl = document.getElementById('weatherResult');
    if (!city) {{
      resultEl.innerHTML = '<span style="color:#b00;">' + MSG_PLEASE_SELECT + '</span>';
      return;
    }}
    fetch(`/weather?city=${{encodeURIComponent(city)}}`)
      .then(r => r.json())
      .then(data => {{
        if (data.cod !== 200 && data.error) {{
          resultEl.innerHTML = `<span style="color:#b00;">${{data.error}}</span>`;
          return;
        }}
        if (data.cod !== 200) {{
          resultEl.innerHTML = '<span style="color:#b00;">' + MSG_NOT_FOUND_TEMPLATE.replace('{{city}}', city) + '</span>';
          return;
        }}
        resultEl.innerHTML = renderWeatherData(data);
      }})
      .catch(() => {{
        document.getElementById('weatherResult').innerHTML = '<span style="color:#b00;">' + MSG_FETCH_ERROR + '</span>';
      }});
  }}

  document.getElementById('cityDropdown').addEventListener('change', function() {{
    document.getElementById('cityInput').value = this.value;
    if (this.value) fetchWeather(this.value);
  }});

  document.getElementById('cityInput').addEventListener('input', function() {{
    const val = this.value.trim();
    const dd = document.getElementById('cityDropdown');
    let found = false;
    for (let i = 0; i < dd.options.length; i++) {{
      if (dd.options[i].value.toLowerCase() === val.toLowerCase()) {{
        dd.selectedIndex = i;
        found = true;
        break;
      }}
    }}
    if (!found) dd.selectedIndex = 0;
  }});

  document.getElementById('weatherForm').addEventListener('submit', function(e) {{
    e.preventDefault();
    const city = document.getElementById('cityInput').value.trim() || document.getElementById('cityDropdown').value;
    fetchWeather(city);
  }});

  document.getElementById('useLocationBtn').addEventListener('click', function() {{
    if (!navigator.geolocation) {{
      document.getElementById('weatherResult').innerHTML = '<span style="color:#b00;">' + MSG_GEO_UNSUPPORTED + '</span>';
      return;
    }}
    navigator.geolocation.getCurrentPosition(function(pos) {{
      const lat = pos.coords.latitude;
      const lon = pos.coords.longitude;
      fetch(`/weather?lat=${{lat}}&lon=${{lon}}`)
        .then(r => r.json())
        .then(data => {{
          if (data.cod !== 200 && data.error) {{
            document.getElementById('weatherResult').innerHTML = `<span style="color:#b00;">${{data.error}}</span>`;
            return;
          }}
          if (data.cod !== 200) {{
            document.getElementById('weatherResult').innerHTML = '<span style="color:#b00;">' + MSG_UNABLE_LOCATION + '</span>';
            return;
          }}
          document.getElementById('weatherResult').innerHTML = renderWeatherData(data);
          document.getElementById('cityInput').value = data.name;
          document.getElementById('cityDropdown').value = '';
        }})
        .catch(() => {{
          document.getElementById('weatherResult').innerHTML = '<span style="color:#b00;">' + MSG_FETCH_ERROR + '</span>';
        }});
    }}, function() {{
      document.getElementById('weatherResult').innerHTML = '<span style="color:#b00;">' + MSG_UNABLE_LOCATION + '</span>';
    }});
  }});

  // language selector redirect
  (function() {{
    var sel = document.getElementById('language-select-top');
    if (sel) {{
      sel.addEventListener('change', function() {{
        var v = this.value || 'en';
        window.location.href = 'weather-' + v + '.html';
      }});
    }}
  }})();
  </script>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/js/all.min.js"></script>
</body>
</html>
"""
    return html_out


def generate_article_html(code: str, section: Dict, page_type: str) -> str:
    dir_attr = ' dir="rtl"' if code == "ar" else ""
    title = escape_allow_tags(section.get("title", ""))
    desc = escape_allow_tags(section.get("desc", ""))
    back_link = section.get("back_link", f"weather-{code}.html")
    back_btn = escape_allow_tags(section.get("back_btn", "Back to Weather"))

    if page_type == "howto":
        heading = escape_allow_tags(section.get("steps_title", "How to use"))
        body_list = "\n".join(f"<li>{escape_allow_tags(s)}</li>" for s in section.get("steps", []))
        extra = f"""
      <h2>{heading}</h2>
      <ol>
        {body_list}
      </ol>
"""
    else:
        heading = escape_allow_tags(section.get("tips_title", "Top Tips"))
        body_list = "\n".join(f"<li>{escape_allow_tags(t)}</li>" for t in section.get("tips", []))
        extra = f"""
      <h2>{heading}</h2>
      <ul>
        {body_list}
      </ul>
"""

    html_out = f"""<!doctype html>
<html lang="{code}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <style>
    body {{ background:#f4f7fb; font-family:'Montserrat', Arial, sans-serif; color:#0b2545; }}
    .page {{ max-width:820px; margin:2.2rem auto; padding:0 1rem; }}
    .article-card {{ background:#fff; border-radius:14px; padding:2rem; box-shadow:0 6px 18px rgba(11,37,69,0.06); }}
    a.back-link {{ color:#0d6efd; font-weight:600; display:inline-block; margin-bottom:1rem; text-decoration:none; }}
    h1.title {{ color:#185a9d; font-size:2rem; margin-bottom:.4rem; }}
    p.lead {{ color:#374151; margin-bottom:1rem; }}
    h2 {{ font-size:1.25rem; margin-top:1rem; margin-bottom:.6rem; }}
    ul, ol {{ color:#374151; padding-left:1.2rem; }}
    .back-bottom {{ margin-top:1.25rem; display:inline-block; }}
    footer.site {{ color:#6b7280; margin-top:1.5rem; text-align:center; }}

    /* Keep article pages consistent: no underlines inside article-card lists (even on hover) */
    .article-card a,
    .article-card ul a,
    .article-card ol a,
    .article-card li a,
    .article-card ul li a,
    .article-card ol li a {{
      text-decoration: none !important;
      color: inherit !important;
    }}
    .article-card a:hover,
    .article-card ul a:hover,
    .article-card ol a:hover,
    .article-card li a:hover,
    .article-card ul li a:hover,
    .article-card ol li a:hover {{
      text-decoration: none !important;
      color: inherit !important;
    }}
    @media (max-width:900px) {{ .page {{ margin:1rem auto; }} .article-card {{ padding:1rem; }} h1.title {{ font-size:1.6rem; }} }}
  </style>
</head>
<body>
  <div class="page">
    <a class="back-link" href="{back_link}">&larr; {back_btn}</a>

    <div class="article-card">
      <h1 class="title">{title}</h1>
      <p class="lead">{desc}</p>

      {extra}

      <a class="btn btn-outline-primary back-bottom" href="{back_link}">{back_btn}</a>
    </div>

    <footer class="site">{section.get('footer','')}</footer>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    return html_out


def generate_redirect_html() -> str:
    html_out = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Global Weather — TimerHaven</title>
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0;url=weather-en.html">
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; padding: 2rem; background:#f7f9fb; color:#0b2545; }
    .box { max-width:720px; margin:3rem auto; background:#fff; padding:1.5rem; border-radius:10px; box-shadow:0 6px 18px rgba(11,37,69,0.06); }
    a { color:#0d6efd; text-decoration:none; }
  </style>
  <script>
    (function(){
      var map = {
        'en': 'weather-en.html',
        'fr': 'weather-fr.html',
        'es': 'weather-es.html',
        'de': 'weather-de.html',
        'ru': 'weather-ru.html',
        'el': 'weather-el.html',
        'ar': 'weather-ar.html'
      };
      function getQueryLang() {
        try {
          var m = location.search.match(/[?&]lang=([a-z]{2})/i);
          return m ? m[1].toLowerCase() : null;
        } catch (e) { return null; }
      }
      function pickByNavigator() {
        var langs = [];
        try {
          if (navigator.languages) langs = langs.concat(navigator.languages);
          if (navigator.language) langs.push(navigator.language);
          if (navigator.userLanguage) langs.push(navigator.userLanguage);
        } catch (e) {}
        for (var i=0;i<langs.length;i++) {
          if (!langs[i]) continue;
          var code = String(langs[i]).toLowerCase().split('-')[0];
          if (map[code]) return code;
        }
        return null;
      }
      var q = getQueryLang();
      if (q && map[q]) { window.location.replace(map[q]); return; }
      var d = pickByNavigator();
      if (d && map[d]) { window.location.replace(map[d]); return; }
      window.location.replace(map['en']);
    })();
  </script>
</head>
<body>
  <div class="box">
    <h1>Global Weather — TimerHaven</h1>
    <p>If you are not redirected automatically, choose a language:</p>
    <ul>
      <li><a href="weather-en.html">English</a></li>
      <li><a href="weather-fr.html">Français</a></li>
      <li><a href="weather-es.html">Español</a></li>
      <li><a href="weather-de.html">Deutsch</a></li>
      <li><a href="weather-ru.html">Русский</a></li>
      <li><a href="weather-el.html">Ελληνικά</a></li>
      <li><a href="weather-ar.html">العربية</a></li>
    </ul>
  </div>
</body>
</html>
"""
    return html_out


def write_files(write_root_redirect: bool = False) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for code, data in TRANSLATIONS.items():
        data.setdefault("howto", {})
        data.setdefault("tips", {})
        data["howto"].setdefault("back_link", f"weather-{code}.html")
        data["tips"].setdefault("back_link", f"weather-{code}.html")

        main_path = os.path.join(OUTPUT_DIR, f"weather-{code}.html")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(generate_main_html(code, data))

        howto_path = os.path.join(OUTPUT_DIR, f"weather-how-to-{code}.html")
        with open(howto_path, "w", encoding="utf-8") as f:
            f.write(generate_article_html(code, data["howto"], "howto"))

        tips_path = os.path.join(OUTPUT_DIR, f"weather-tips-{code}.html")
        with open(tips_path, "w", encoding="utf-8") as f:
            f.write(generate_article_html(code, data["tips"], "tips"))

    redirect_path = os.path.join(OUTPUT_DIR, "weather.html")
    with open(redirect_path, "w", encoding="utf-8") as f:
        f.write(generate_redirect_html())

    if write_root_redirect:
        with open("weather.html", "w", encoding="utf-8") as f:
            f.write(generate_redirect_html())

    print(f"All pages generated successfully in the '{OUTPUT_DIR}' folder.")
    if write_root_redirect:
        print(f"Root redirect written to '{os.path.abspath('weather.html')}'.")


def main(argv: List[str] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]
    write_root = False
    if "--root" in argv or "-r" in argv:
        write_root = True
    write_files(write_root_redirect=write_root)


if __name__ == "__main__":
    main()