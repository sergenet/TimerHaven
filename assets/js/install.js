/**
 * TimerHaven install + pinning helper.
 *
 * Every tool page carries its own web app manifest, so installing from a tool
 * page gives the visitor their own icon that opens straight into that tool —
 * the browser equivalent of the Android app's pinned shortcut.
 */
(function () {
  "use strict";

  var script = document.currentScript;
  var manifestUrl =
    (script && script.getAttribute("data-th-scheme")) ||
    (document.querySelector('link[rel="manifest"]') || {}).href ||
    "/manifest.json";

  var I18N = {
    en: {
      install: "Install app",
      pin: "Pin {name}",
      title: "Add {name} to your device",
      intro: "Then {name} opens straight from your home screen, full screen, without the browser.",
      chrome: "Chrome or Edge: open the \u22ee menu and choose \u201cInstall app\u201d or \u201cAdd to Home screen\u201d.",
      ios: "iPhone or iPad (Safari): tap the Share button, then \u201cAdd to Home Screen\u201d.",
      android: "Android browser: open the \u22ee menu and tap \u201cAdd to Home screen\u201d.",
      close: "Close",
      store: "Get the Android app",
      done: "{name} added to your home screen.",
      failed: "Your browser did not offer an install prompt. Use the menu steps below."
    },
    de: {
      install: "App installieren",
      pin: "{name} anheften",
      title: "{name} zum Startbildschirm hinzuf\u00fcgen",
      intro: "Danach \u00f6ffnet sich {name} direkt vom Startbildschirm \u2013 im Vollbild, ohne Browser.",
      chrome: "Chrome oder Edge: \u22ee-Men\u00fc \u00f6ffnen und \u201eApp installieren\u201c bzw. \u201eZum Startbildschirm hinzuf\u00fcgen\u201c w\u00e4hlen.",
      ios: "iPhone oder iPad (Safari): Teilen-Symbol antippen, dann \u201eZum Startbildschirm\u201c.",
      android: "Android-Browser: \u22ee-Men\u00fc \u00f6ffnen und \u201eZum Startbildschirm hinzuf\u00fcgen\u201c antippen.",
      close: "Schlie\u00dfen",
      store: "Android-App holen",
      done: "{name} wurde hinzugef\u00fcgt.",
      failed: "Der Browser hat keinen Installationsdialog angeboten. Nutze die Schritte unten."
    },
    el: {
      install: "\u0395\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7",
      pin: "\u039a\u03b1\u03c1\u03c6\u03af\u03c4\u03c3\u03c9\u03c3\u03b5 {name}",
      title: "\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7 {name} \u03c3\u03c4\u03b7\u03bd \u03b1\u03c1\u03c7\u03b9\u03ba\u03ae \u03bf\u03b8\u03cc\u03bd\u03b7",
      intro: "\u039c\u03b5\u03c4\u03ac, \u03c4\u03bf {name} \u03b1\u03bd\u03bf\u03af\u03b3\u03b5\u03b9 \u03b1\u03c0\u03b5\u03c5\u03b8\u03b5\u03af\u03b1\u03c2 \u03b1\u03c0\u03cc \u03c4\u03b7\u03bd \u03b1\u03c1\u03c7\u03b9\u03ba\u03ae \u03bf\u03b8\u03cc\u03bd\u03b7, \u03c7\u03c9\u03c1\u03af\u03c2 \u03c0\u03b5\u03c1\u03b9\u03b7\u03b3\u03b7\u03c4\u03ae.",
      chrome: "Chrome \u03ae Edge: \u03ac\u03bd\u03bf\u03b9\u03be\u03b5 \u03c4\u03bf \u03bc\u03b5\u03bd\u03bf\u03cd \u22ee \u03ba\u03b1\u03b9 \u03b5\u03c0\u03ad\u03bb\u03b5\u03be\u03b5 \u00ab\u0395\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7 \u03b5\u03c6\u03b1\u03c1\u03bc\u03bf\u03b3\u03ae\u03c2\u00bb.",
      ios: "iPhone \u03ae iPad (Safari): \u03c0\u03ac\u03c4\u03b1 \u039a\u03bf\u03b9\u03bd\u03ae \u03c7\u03c1\u03ae\u03c3\u03b7, \u03bc\u03b5\u03c4\u03ac \u00ab\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7 \u03c3\u03c4\u03b7\u03bd \u03b1\u03c1\u03c7\u03b9\u03ba\u03ae \u03bf\u03b8\u03cc\u03bd\u03b7\u00bb.",
      android: "Android: \u03ac\u03bd\u03bf\u03b9\u03be\u03b5 \u03c4\u03bf \u03bc\u03b5\u03bd\u03bf\u03cd \u22ee \u03ba\u03b1\u03b9 \u03c0\u03ac\u03c4\u03b1 \u00ab\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7 \u03c3\u03c4\u03b7\u03bd \u03b1\u03c1\u03c7\u03b9\u03ba\u03ae \u03bf\u03b8\u03cc\u03bd\u03b7\u00bb.",
      close: "\u039a\u03bb\u03b5\u03af\u03c3\u03b9\u03bc\u03bf",
      store: "\u0391\u03c0\u03bf\u03ba\u03c4\u03ae\u03c3\u03c4\u03b5 \u03c4\u03b7\u03bd \u03b5\u03c6\u03b1\u03c1\u03bc\u03bf\u03b3\u03ae Android",
      done: "\u03a4\u03bf {name} \u03c0\u03c1\u03bf\u03c3\u03c4\u03ad\u03b8\u03b7\u03ba\u03b5.",
      failed: "\u039f \u03c0\u03b5\u03c1\u03b9\u03b7\u03b3\u03b7\u03c4\u03ae\u03c2 \u03b4\u03b5\u03bd \u03c0\u03c1\u03cc\u03c4\u03b5\u03b9\u03bd\u03b5 \u03b5\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7. \u0391\u03ba\u03bf\u03bb\u03bf\u03cd\u03b8\u03b7\u03c3\u03b5 \u03c4\u03b1 \u03b2\u03ae\u03bc\u03b1\u03c4\u03b1."
    },
    es: {
      install: "Instalar app",
      pin: "Fijar {name}",
      title: "A\u00f1adir {name} a tu pantalla de inicio",
      intro: "Despu\u00e9s, {name} se abre directamente desde tu pantalla de inicio, a pantalla completa y sin navegador.",
      chrome: "Chrome o Edge: abre el men\u00fa \u22ee y elige \u00abInstalar aplicaci\u00f3n\u00bb o \u00abA\u00f1adir a pantalla de inicio\u00bb.",
      ios: "iPhone o iPad (Safari): toca Compartir y luego \u00abA\u00f1adir a pantalla de inicio\u00bb.",
      android: "Navegador Android: abre el men\u00fa \u22ee y toca \u00abA\u00f1adir a pantalla de inicio\u00bb.",
      close: "Cerrar",
      store: "Descargar la app de Android",
      done: "{name} se a\u00f1adi\u00f3 a tu pantalla de inicio.",
      failed: "El navegador no ofreci\u00f3 instalar. Sigue los pasos de abajo."
    },
    fr: {
      install: "Installer l'app",
      pin: "\u00c9pingler {name}",
      title: "Ajouter {name} \u00e0 votre \u00e9cran d'accueil",
      intro: "Ensuite, {name} s'ouvre directement depuis votre \u00e9cran d'accueil, en plein \u00e9cran, sans navigateur.",
      chrome: "Chrome ou Edge\u00a0: ouvrez le menu \u22ee et choisissez \u00ab\u00a0Installer l'application\u00a0\u00bb ou \u00ab\u00a0Ajouter \u00e0 l'\u00e9cran d'accueil\u00a0\u00bb.",
      ios: "iPhone ou iPad (Safari)\u00a0: touchez Partager, puis \u00ab\u00a0Sur l'\u00e9cran d'accueil\u00a0\u00bb.",
      android: "Navigateur Android\u00a0: ouvrez le menu \u22ee et touchez \u00ab\u00a0Ajouter \u00e0 l'\u00e9cran d'accueil\u00a0\u00bb.",
      close: "Fermer",
      store: "Obtenir l'app Android",
      done: "{name} a \u00e9t\u00e9 ajout\u00e9 \u00e0 votre \u00e9cran d'accueil.",
      failed: "Le navigateur n'a pas propos\u00e9 d'installation. Suivez les \u00e9tapes ci-dessous."
    },
    ru: {
      install: "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c",
      pin: "\u0417\u0430\u043a\u0440\u0435\u043f\u0438\u0442\u044c {name}",
      title: "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c {name} \u043d\u0430 \u0433\u043b\u0430\u0432\u043d\u044b\u0439 \u044d\u043a\u0440\u0430\u043d",
      intro: "\u041f\u043e\u0441\u043b\u0435 \u044d\u0442\u043e\u0433\u043e {name} \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u0441\u0440\u0430\u0437\u0443 \u0441 \u0433\u043b\u0430\u0432\u043d\u043e\u0433\u043e \u044d\u043a\u0440\u0430\u043d\u0430, \u043d\u0430 \u0432\u0435\u0441\u044c \u044d\u043a\u0440\u0430\u043d \u0438 \u0431\u0435\u0437 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0430.",
      chrome: "Chrome \u0438\u043b\u0438 Edge: \u043e\u0442\u043a\u0440\u043e\u0439\u0442\u0435 \u043c\u0435\u043d\u044e \u22ee \u0438 \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u00ab\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435\u00bb.",
      ios: "iPhone \u0438\u043b\u0438 iPad (Safari): \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u00ab\u041f\u043e\u0434\u0435\u043b\u0438\u0442\u044c\u0441\u044f\u00bb, \u0437\u0430\u0442\u0435\u043c \u00ab\u041d\u0430 \u044d\u043a\u0440\u0430\u043d \u00ab\u0414\u043e\u043c\u043e\u0439\u00bb\u00bb.",
      android: "\u0411\u0440\u0430\u0443\u0437\u0435\u0440 Android: \u043e\u0442\u043a\u0440\u043e\u0439\u0442\u0435 \u043c\u0435\u043d\u044e \u22ee \u0438 \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u00ab\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043d\u0430 \u0433\u043b\u0430\u0432\u043d\u044b\u0439 \u044d\u043a\u0440\u0430\u043d\u00bb.",
      close: "\u0417\u0430\u043a\u0440\u044b\u0442\u044c",
      store: "\u0421\u043a\u0430\u0447\u0430\u0442\u044c \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u0434\u043b\u044f Android",
      done: "{name} \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u043e \u043d\u0430 \u0433\u043b\u0430\u0432\u043d\u044b\u0439 \u044d\u043a\u0440\u0430\u043d.",
      failed: "\u0411\u0440\u0430\u0443\u0437\u0435\u0440 \u043d\u0435 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0438\u043b \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0443. \u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0439\u0442\u0435 \u0448\u0430\u0433\u0438 \u043d\u0438\u0436\u0435."
    },
    ar: {
      install: "\u062a\u062b\u0628\u064a\u062a \u0627\u0644\u062a\u0637\u0628\u064a\u0642",
      pin: "\u062a\u062b\u0628\u064a\u062a {name}",
      title: "\u0625\u0636\u0627\u0641\u0629 {name} \u0625\u0644\u0649 \u0627\u0644\u0634\u0627\u0634\u0629 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629",
      intro: "\u0628\u0639\u062f \u0630\u0644\u0643 \u064a\u0641\u062a\u062d {name} \u0645\u0628\u0627\u0634\u0631\u0629\u064b \u0645\u0646 \u0627\u0644\u0634\u0627\u0634\u0629 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629\u060c \u0628\u062f\u0648\u0646 \u0645\u062a\u0635\u0641\u062d.",
      chrome: "Chrome \u0623\u0648 Edge: \u0627\u0641\u062a\u062d \u0642\u0627\u0626\u0645\u0629 \u22ee \u0648\u0627\u062e\u062a\u0631 \u00ab\u062a\u062b\u0628\u064a\u062a \u0627\u0644\u062a\u0637\u0628\u064a\u0642\u00bb.",
      ios: "iPhone \u0623\u0648 iPad (Safari): \u0627\u0636\u063a\u0637 \u0632\u0631 \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u0629 \u062b\u0645 \u00ab\u0625\u0636\u0627\u0641\u0629 \u0625\u0644\u0649 \u0627\u0644\u0634\u0627\u0634\u0629 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629\u00bb.",
      android: "\u0645\u062a\u0635\u0641\u062d Android: \u0627\u0641\u062a\u062d \u0627\u0644\u0642\u0627\u0626\u0645\u0629 \u22ee \u0648\u0627\u0636\u063a\u0637 \u00ab\u0625\u0636\u0627\u0641\u0629 \u0625\u0644\u0649 \u0627\u0644\u0634\u0627\u0634\u0629 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629\u00bb.",
      close: "\u0625\u063a\u0644\u0627\u0642",
      store: "\u0627\u0644\u062d\u0635\u0648\u0644 \u0639\u0644\u0649 \u062a\u0637\u0628\u064a\u0642 \u0623\u0646\u062f\u0631\u0648\u064a\u062f",
      done: "\u062a\u0645\u062a \u0625\u0636\u0627\u0641\u0629 {name} \u0625\u0644\u0649 \u0627\u0644\u0634\u0627\u0634\u0629 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629.",
      failed: "\u0644\u0645 \u064a\u0642\u062f\u0645 \u0627\u0644\u0645\u062a\u0635\u0641\u062d \u062e\u064a\u0627\u0631 \u0627\u0644\u062a\u062b\u0628\u064a\u062a. \u0627\u062a\u0628\u0639 \u0627\u0644\u062e\u0637\u0648\u0627\u062a \u0623\u062f\u0646\u0627\u0647."
    }
  };

  // Desktop visitors install an app window rather than a home-screen icon, so
  // the wording for computers lives apart from the mobile copy above.
  var DESKTOP = {
    en: {
      title: "Install {name} on your computer",
      intro: "It opens in its own window, straight into {name}, without browser tabs. Then pin it wherever you keep your apps.",
      step: "Chrome or Edge: menu \u22ee \u2192 \u201cInstall app\u201d. Safari on Mac: File \u2192 \u201cAdd to Dock\u201d. Right-click the new icon to pin it to the taskbar, desktop or Dock.",
      done: "{name} installed. Pin it from your taskbar, desktop or Dock."
    },
    de: {
      title: "{name} auf deinem Computer installieren",
      intro: "Es \u00f6ffnet sich in einem eigenen Fenster, direkt in {name}, ohne Browser-Tabs. Anschlie\u00dfend kannst du es anheften, wo du deine Apps ablegst.",
      step: "Chrome oder Edge: Men\u00fc \u22ee \u2192 \u201eApp installieren\u201c. Safari am Mac: Datei \u2192 \u201eZum Dock hinzuf\u00fcgen\u201c. Rechtsklick auf das neue Symbol, um es an Taskleiste, Desktop oder Dock anzuheften.",
      done: "{name} ist installiert. Hefte es \u00fcber Taskleiste, Desktop oder Dock an."
    },
    el: {
      title: "\u0395\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7 \u03c4\u03bf\u03c5 {name} \u03c3\u03c4\u03bf\u03bd \u03c5\u03c0\u03bf\u03bb\u03bf\u03b3\u03b9\u03c3\u03c4\u03ae \u03c3\u03b1\u03c2",
      intro: "\u0391\u03bd\u03bf\u03af\u03b3\u03b5\u03b9 \u03c3\u03b5 \u03b4\u03b9\u03ba\u03cc \u03c4\u03bf\u03c5 \u03c0\u03b1\u03c1\u03ac\u03b8\u03c5\u03c1\u03bf, \u03b1\u03c0\u03b5\u03c5\u03b8\u03b5\u03af\u03b1\u03c2 \u03c3\u03c4\u03bf {name}, \u03c7\u03c9\u03c1\u03af\u03c2 \u03ba\u03b1\u03c1\u03c4\u03ad\u03bb\u03b5\u03c2. \u03a3\u03c4\u03b7 \u03c3\u03c5\u03bd\u03ad\u03c7\u03b5\u03b9\u03b1 \u03ba\u03b1\u03c1\u03c6\u03b9\u03c4\u03c3\u03ce\u03c3\u03c4\u03b5 \u03c4\u03bf \u03b5\u03ba\u03b5\u03af \u03c0\u03bf\u03c5 \u03ba\u03c1\u03b1\u03c4\u03ac\u03c4\u03b5 \u03c4\u03b9\u03c2 \u03b5\u03c6\u03b1\u03c1\u03bc\u03bf\u03b3\u03ad\u03c2 \u03c3\u03b1\u03c2.",
      step: "Chrome \u03ae Edge: \u03bc\u03b5\u03bd\u03bf\u03cd \u22ee \u2192 \u00ab\u0395\u03b3\u03ba\u03b1\u03c4\u03ac\u03c3\u03c4\u03b1\u03c3\u03b7 \u03b5\u03c6\u03b1\u03c1\u03bc\u03bf\u03b3\u03ae\u03c2\u00bb. Safari \u03c3\u03b5 Mac: \u0391\u03c1\u03c7\u03b5\u03af\u03bf \u2192 \u00ab\u03a0\u03c1\u03bf\u03c3\u03b8\u03ae\u03ba\u03b7 \u03c3\u03c4\u03bf Dock\u00bb. \u039a\u03ac\u03bd\u03c4\u03b5 \u03b4\u03b5\u03be\u03af \u03ba\u03bb\u03b9\u03ba \u03c3\u03c4\u03bf \u03bd\u03ad\u03bf \u03b5\u03b9\u03ba\u03bf\u03bd\u03af\u03b4\u03b9\u03bf \u03b3\u03b9\u03b1 \u03ba\u03b1\u03c1\u03c6\u03af\u03c4\u03c3\u03c9\u03bc\u03b1 \u03c3\u03c4\u03b7 \u03b3\u03c1\u03b1\u03bc\u03bc\u03ae \u03b5\u03c1\u03b3\u03b1\u03c3\u03b9\u03ce\u03bd, \u03c4\u03b7\u03bd \u03b5\u03c0\u03b9\u03c6\u03ac\u03bd\u03b5\u03b9\u03b1 \u03b5\u03c1\u03b3\u03b1\u03c3\u03af\u03b1\u03c2 \u03ae \u03c4\u03bf Dock.",
      done: "\u03a4\u03bf {name} \u03b5\u03b3\u03ba\u03b1\u03c4\u03b1\u03c3\u03c4\u03ac\u03b8\u03b7\u03ba\u03b5. \u039a\u03b1\u03c1\u03c6\u03b9\u03c4\u03c3\u03ce\u03c3\u03c4\u03b5 \u03c4\u03bf \u03b1\u03c0\u03cc \u03c4\u03b7 \u03b3\u03c1\u03b1\u03bc\u03bc\u03ae \u03b5\u03c1\u03b3\u03b1\u03c3\u03b9\u03ce\u03bd, \u03c4\u03b7\u03bd \u03b5\u03c0\u03b9\u03c6\u03ac\u03bd\u03b5\u03b9\u03b1 \u03b5\u03c1\u03b3\u03b1\u03c3\u03af\u03b1\u03c2 \u03ae \u03c4\u03bf Dock."
    },
    es: {
      title: "Instalar {name} en tu ordenador",
      intro: "Se abre en su propia ventana, directamente en {name}, sin pesta\u00f1as. Luego f\u00edjalo donde guardes tus aplicaciones.",
      step: "Chrome o Edge: men\u00fa \u22ee \u2192 \u00abInstalar aplicaci\u00f3n\u00bb. Safari en Mac: Archivo \u2192 \u00abA\u00f1adir al Dock\u00bb. Haz clic derecho en el nuevo icono para fijarlo a la barra de tareas, el escritorio o el Dock.",
      done: "{name} se instal\u00f3. F\u00edjalo desde la barra de tareas, el escritorio o el Dock."
    },
    fr: {
      title: "Installer {name} sur votre ordinateur",
      intro: "Il s'ouvre dans sa propre fen\u00eatre, directement sur {name}, sans onglets. \u00c9pinglez-le ensuite l\u00e0 o\u00f9 vous rangez vos applications.",
      step: "Chrome ou Edge\u00a0: menu \u22ee \u2192 \u00ab\u00a0Installer l'application\u00a0\u00bb. Safari sur Mac\u00a0: Fichier \u2192 \u00ab\u00a0Ajouter au Dock\u00a0\u00bb. Faites un clic droit sur la nouvelle ic\u00f4ne pour l'\u00e9pingler \u00e0 la barre des t\u00e2ches, au bureau ou au Dock.",
      done: "{name} est install\u00e9. \u00c9pinglez-le depuis la barre des t\u00e2ches, le bureau ou le Dock."
    },
    ru: {
      title: "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c {name} \u043d\u0430 \u043a\u043e\u043c\u043f\u044c\u044e\u0442\u0435\u0440",
      intro: "\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u0432 \u043e\u0442\u0434\u0435\u043b\u044c\u043d\u043e\u043c \u043e\u043a\u043d\u0435, \u0441\u0440\u0430\u0437\u0443 \u0432 {name}, \u0431\u0435\u0437 \u0432\u043a\u043b\u0430\u0434\u043e\u043a \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0430. \u0417\u0430\u0442\u0435\u043c \u0437\u0430\u043a\u0440\u0435\u043f\u0438\u0442\u0435 \u0435\u0433\u043e \u0442\u0430\u043c, \u0433\u0434\u0435 \u0445\u0440\u0430\u043d\u0438\u0442\u0435 \u0441\u0432\u043e\u0438 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f.",
      step: "Chrome \u0438\u043b\u0438 Edge: \u043c\u0435\u043d\u044e \u22ee \u2192 \u00ab\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435\u00bb. Safari \u043d\u0430 Mac: \u0424\u0430\u0439\u043b \u2192 \u00ab\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432 Dock\u00bb. \u0429\u0451\u043b\u043a\u043d\u0438\u0442\u0435 \u043f\u0440\u0430\u0432\u043e\u0439 \u043a\u043d\u043e\u043f\u043a\u043e\u0439 \u043f\u043e \u043d\u043e\u0432\u043e\u043c\u0443 \u0437\u043d\u0430\u0447\u043a\u0443, \u0447\u0442\u043e\u0431\u044b \u0437\u0430\u043a\u0440\u0435\u043f\u0438\u0442\u044c \u0435\u0433\u043e \u043d\u0430 \u043f\u0430\u043d\u0435\u043b\u0438 \u0437\u0430\u0434\u0430\u0447, \u0440\u0430\u0431\u043e\u0447\u0435\u043c \u0441\u0442\u043e\u043b\u0435 \u0438\u043b\u0438 \u0432 Dock.",
      done: "{name} \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043e. \u0417\u0430\u043a\u0440\u0435\u043f\u0438\u0442\u0435 \u0435\u0433\u043e \u043d\u0430 \u043f\u0430\u043d\u0435\u043b\u0438 \u0437\u0430\u0434\u0430\u0447, \u0440\u0430\u0431\u043e\u0447\u0435\u043c \u0441\u0442\u043e\u043b\u0435 \u0438\u043b\u0438 \u0432 Dock."
    },
    ar: {
      title: "\u062a\u062b\u0628\u064a\u062a {name} \u0639\u0644\u0649 \u062c\u0647\u0627\u0632 \u0627\u0644\u0643\u0645\u0628\u064a\u0648\u062a\u0631",
      intro: "\u064a\u0641\u062a\u062d \u0641\u064a \u0646\u0627\u0641\u0630\u0629 \u062e\u0627\u0635\u0629 \u0628\u0647\u060c \u0645\u0628\u0627\u0634\u0631\u0629\u064b \u0639\u0644\u0649 {name}\u060c \u062f\u0648\u0646 \u0639\u0644\u0627\u0645\u0627\u062a \u062a\u0628\u0648\u064a\u0628. \u062b\u0645 \u062b\u0628\u0651\u062a\u0647 \u062d\u064a\u062b \u062a\u062d\u0641\u0638 \u062a\u0637\u0628\u064a\u0642\u0627\u062a\u0643.",
      step: "Chrome \u0623\u0648 Edge: \u0627\u0644\u0642\u0627\u0626\u0645\u0629 \u22ee \u2190 \u00ab\u062a\u062b\u0628\u064a\u062a \u0627\u0644\u062a\u0637\u0628\u064a\u0642\u00bb. Safari \u0639\u0644\u0649 Mac: \u0645\u0644\u0641 \u2190 \u00ab\u0625\u0636\u0627\u0641\u0629 \u0625\u0644\u0649 Dock\u00bb. \u0627\u0646\u0642\u0631 \u0628\u0632\u0631 \u0627\u0644\u0641\u0623\u0631\u0629 \u0627\u0644\u0623\u064a\u0645\u0646 \u0639\u0644\u0649 \u0627\u0644\u0623\u064a\u0642\u0648\u0646\u0629 \u0627\u0644\u062c\u062f\u064a\u062f\u0629 \u0644\u062a\u062b\u0628\u064a\u062a\u0647\u0627 \u0641\u064a \u0634\u0631\u064a\u0637 \u0627\u0644\u0645\u0647\u0627\u0645 \u0623\u0648 \u0633\u0637\u062d \u0627\u0644\u0645\u0643\u062a\u0628 \u0623\u0648 Dock.",
      done: "\u062a\u0645 \u062a\u062b\u0628\u064a\u062a {name}. \u062b\u0628\u0651\u062a\u0647 \u0645\u0646 \u0634\u0631\u064a\u0637 \u0627\u0644\u0645\u0647\u0627\u0645 \u0623\u0648 \u0633\u0637\u062d \u0627\u0644\u0645\u0643\u062a\u0628 \u0623\u0648 Dock."
    }
  };

  var tool = (script && script.getAttribute("data-th-tool")) || "home";
  var htmlLang = (document.documentElement.lang || "en").slice(0, 2).toLowerCase();
  var t = I18N[htmlLang] || I18N.en;
  var d = DESKTOP[htmlLang] || DESKTOP.en;
  var desktop = isDesktop();
  var appName = "TimerHaven";
  var shortName = "TimerHaven";
  var promptEvent = null;
  var installedKey = "th-installed:" + manifestUrl;

  function fill(text) {
    return String(text).replace(/\{name\}/g, shortName);
  }

  // Google Play listing for the Android app. The Play install referrer carries
  // this URL's `referrer` parameter into the app on first launch, so the
  // acquisition report shows which tool page sent the visitor and in which
  // language (`utm_campaign=pomodoro_de`). Campaign values tolerate only
  // letters, digits and underscores - anything else truncates the match.
  var PLAY_PACKAGE = "com.sergenet.TimerHavenApp";

  function storeUrl() {
    var campaign = (tool + "_" + htmlLang).replace(/[^a-z0-9_]/gi, "");
    return (
      "https://play.google.com/store/apps/details?id=" +
      PLAY_PACKAGE +
      "&referrer=" +
      encodeURIComponent(
        "utm_source=timerhaven_site&utm_medium=install_sheet&utm_campaign=" + campaign
      )
    );
  }

  function isStandalone() {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.matchMedia("(display-mode: minimal-ui)").matches ||
      window.navigator.standalone === true
    );
  }

  function isIos() {
    return (
      /iPad|iPhone|iPod/.test(navigator.userAgent) ||
      (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1)
    );
  }

  // Desktop browsers install into their own app window; phones and tablets add a
  // home-screen icon. iPadOS reports itself as a Mac, so isIos() has to win first.
  function isDesktop() {
    if (isIos()) return false;
    return !/Android|Mobile|IEMobile|Opera Mini/i.test(navigator.userAgent);
  }

  function registerServiceWorker() {
    if (!("serviceWorker" in navigator)) return;
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js").catch(function () {
        /* offline support is optional; never break the page over it */
      });
    });
  }

  function buildPill() {
    var pill = document.createElement("button");
    pill.type = "button";
    pill.className = "th-install-pill";
    pill.setAttribute("data-th-install", tool);
    pill.innerHTML =
      '<span class="th-install-pill__icon" aria-hidden="true">' +
      '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M4 19h16"/>' +
      "</svg></span><span class=\"th-install-pill__text\"></span>";
    pill.querySelector(".th-install-pill__text").textContent =
      tool === "home" ? t.install : fill(t.pin);
    pill.addEventListener("click", onClick);
    return pill;
  }

  function buildSheet() {
    var sheet = document.createElement("div");
    sheet.className = "th-install-sheet";
    sheet.setAttribute("role", "dialog");
    sheet.setAttribute("aria-modal", "true");
    sheet.hidden = true;
    sheet.innerHTML =
      '<div class="th-install-sheet__backdrop" data-th-close></div>' +
      '<div class="th-install-sheet__panel" role="document">' +
      '<h2 class="th-install-sheet__title"></h2>' +
      '<p class="th-install-sheet__intro"></p>' +
      '<p class="th-install-sheet__step" data-step="desktop"></p>' +
      '<p class="th-install-sheet__step" data-step="ios"></p>' +
      '<p class="th-install-sheet__step" data-step="chrome"></p>' +
      '<p class="th-install-sheet__step" data-step="android"></p>' +
      '<a class="th-install-sheet__store" data-th-store rel="noopener" target="_blank"></a>' +
      '<button type="button" class="th-install-sheet__close" data-th-close></button>' +
      "</div>";
    var copy = desktop ? d : t;
    sheet.querySelector(".th-install-sheet__title").textContent = fill(copy.title);
    sheet.querySelector(".th-install-sheet__intro").textContent = fill(copy.intro);
    sheet.querySelector('[data-step="ios"]').textContent = t.ios;
    sheet.querySelector('[data-step="chrome"]').textContent = t.chrome;
    sheet.querySelector('[data-step="android"]').textContent = t.android;
    var desktopStep = sheet.querySelector('[data-step="desktop"]');
    desktopStep.textContent = d.step;
    if (desktop) {
      // A computer has no home screen, and the Play link is for phones.
      ["ios", "chrome", "android"].forEach(function (step) {
        var el = sheet.querySelector('[data-step="' + step + '"]');
        if (el) el.remove();
      });
    } else {
      desktopStep.remove();
    }
    sheet.querySelector(".th-install-sheet__close").textContent = t.close;
    var store = sheet.querySelector("[data-th-store]");
    if (isIos() || desktop) {
      // No App Store build exists yet, so the link would be a dead end there.
      store.remove();
    } else {
      store.textContent = t.store;
      store.href = storeUrl();
    }
    Array.prototype.forEach.call(sheet.querySelectorAll("[data-th-close]"), function (el) {
      el.addEventListener("click", function () {
        sheet.hidden = true;
      });
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") sheet.hidden = true;
    });
    return sheet;
  }

  function toast(message) {
    var node = document.createElement("div");
    node.className = "th-install-toast";
    node.setAttribute("role", "status");
    node.textContent = message;
    document.body.appendChild(node);
    window.setTimeout(function () {
      node.classList.add("is-leaving");
      window.setTimeout(function () {
        node.remove();
      }, 400);
    }, 4000);
  }

  function onClick() {
    if (promptEvent) {
      promptEvent.prompt();
      promptEvent.userChoice.then(function (choice) {
        if (choice.outcome === "accepted") {
          hidePill();
        }
        promptEvent = null;
      }).catch(function () {
        promptEvent = null;
        showSheet();
      });
      return;
    }
    showSheet();
  }

  var pill = null;
  var sheet = null;

  function showSheet() {
    if (!sheet) {
      sheet = buildSheet();
      document.body.appendChild(sheet);
    }
    sheet.hidden = false;
    var close = sheet.querySelector(".th-install-sheet__close");
    if (close) close.focus();
  }

  function hidePill() {
    if (pill) pill.hidden = true;
  }

  function start() {
    registerServiceWorker();

    if (isStandalone() || localStorage.getItem(installedKey) === "1") return;

    fetch(manifestUrl, { credentials: "same-origin" })
      .then(function (response) {
        return response.ok ? response.json() : null;
      })
      .then(function (data) {
        if (data) {
          appName = data.name || appName;
          shortName = data.short_name || appName;
        }
        pill = buildPill();
        document.body.appendChild(pill);
      })
      .catch(function () {
        pill = buildPill();
        document.body.appendChild(pill);
      });

    window.addEventListener("beforeinstallprompt", function (event) {
      event.preventDefault();
      promptEvent = event;
    });

    window.addEventListener("appinstalled", function () {
      try {
        localStorage.setItem(installedKey, "1");
      } catch (error) {
        /* private mode: nothing to remember */
      }
      hidePill();
      toast(fill(desktop ? d.done : t.done));
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
