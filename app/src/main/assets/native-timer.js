/*
 * Bridges the Pomodoro page to the Android app's native timer.
 *
 * The page stays the thing you look at, but every start/pause/reset is mirrored into
 * PomodoroTimer, which keeps the session alive in the notification and the home-screen widget.
 * On load, a session that is still running is restored into the page.
 */
(function () {
  var bridge = window.AndroidBridge;
  if (!bridge || typeof bridge.timerState !== "function") return;

  function nativeState() {
    try {
      return JSON.parse(bridge.timerState());
    } catch (error) {
      return null;
    }
  }

  function api() {
    return window.TimerHavenPomodoro;
  }

  function hook(id, event, handler) {
    var element = document.getElementById(id);
    if (element) element.addEventListener(event, handler);
  }

  function mirror(kind) {
    var pomodoro = api();
    if (!pomodoro) return;
    var state = pomodoro.getState();

    if (kind === "start") {
      bridge.timerStart(state.workMin, state.breakMin, state.phase, state.remaining);
    } else if (kind === "pause") {
      bridge.timerPause();
    } else if (kind === "reset") {
      bridge.timerReset();
    }
  }

  function onReady() {
    var pomodoro = api();
    var state = nativeState();
    if (pomodoro && state) {
      pomodoro.restore(state);
    }

    hook("startBtn", "click", function () {
      mirror("start");
    });
    hook("pauseBtn", "click", function () {
      mirror("pause");
    });
    hook("resetBtn", "click", function () {
      mirror("reset");
    });

    ["workLength", "breakLength"].forEach(function (id) {
      hook(id, "change", function () {
        var pomodoro = api();
        if (!pomodoro) return;
        var state = pomodoro.getState();
        bridge.timerSetLengths(state.workMin, state.breakMin, state.phase);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
