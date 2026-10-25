package com.emberfront.game;

import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.Insets;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.util.Collections;

/** Offline assets are served at an HTTPS origin. No Internet or file-access permission is needed. */
public final class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final String PREFIX = "/assets/game/";
    private WebView web;
    private boolean exitDialog;

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(0xff10191f);
        web = new WebView(this);
        web.setBackgroundColor(0xff10191f);
        root.addView(web, new FrameLayout.LayoutParams(-1, -1));
        setContentView(root);
        if (Build.VERSION.SDK_INT >= 30) {
            getWindow().setDecorFitsSystemWindows(false);
            root.setOnApplyWindowInsetsListener((v, insets) -> {
                Insets cutout = insets.getInsets(WindowInsets.Type.displayCutout());
                v.setPadding(cutout.left, cutout.top, cutout.right, cutout.bottom);
                return insets;
            });
        }
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setMediaPlaybackRequiresUserGesture(true);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        web.addJavascriptInterface(new Haptics(), "EmberHaptics");
        web.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String path = uri.getPath();
                if (!"GET".equals(request.getMethod()) || !"https".equals(uri.getScheme()) ||
                    !HOST.equals(uri.getHost()) || uri.getPort() != -1 || path == null || !path.startsWith(PREFIX)) return empty(403);
                String relative = path.substring(PREFIX.length());
                for (String segment : relative.split("/")) if (segment.equals("..") || segment.startsWith(".")) return empty(403);
                if (relative.indexOf('\\') >= 0) return empty(403);
                try {
                    String mime = mime(relative);
                    WebResourceResponse response = new WebResourceResponse(mime,
                        mime.startsWith("text/") || mime.equals("application/javascript") || mime.equals("application/json") ? "UTF-8" : null,
                        getAssets().open("game/" + relative));
                    response.setResponseHeaders(Collections.singletonMap("X-Content-Type-Options", "nosniff"));
                    return response;
                } catch (IOException missing) { return empty(404); }
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri u = request.getUrl();
                return !"https".equals(u.getScheme()) || !HOST.equals(u.getHost()) || !u.getPath().startsWith(PREFIX);
            }
            @Override public void onPageFinished(WebView view, String url) {
                web.evaluateJavascript("if(!window.emberSnapshot){document.body.innerHTML='<div style=\"padding:32px;color:white;font:20px sans-serif\">游戏未能启动。请更新 Android System WebView（或 Chrome）后重试。</div>';}", null);
            }
        });
        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(android.window.OnBackInvokedDispatcher.PRIORITY_DEFAULT, this::handleBack);
        }
        web.loadUrl("https://" + HOST + PREFIX + "index.html");
        immersive();
    }

    private WebResourceResponse empty(int code) {
        return new WebResourceResponse("text/plain", "UTF-8", code, code == 404 ? "Not Found" : "Forbidden",
            Collections.emptyMap(), new ByteArrayInputStream(new byte[0]));
    }
    private static String mime(String path) {
        if (path.endsWith(".html")) return "text/html";
        if (path.endsWith(".js")) return "application/javascript";
        if (path.endsWith(".css")) return "text/css";
        if (path.endsWith(".json")) return "application/json";
        if (path.endsWith(".wav")) return "audio/wav";
        if (path.endsWith(".ogg")) return "audio/ogg";
        if (path.endsWith(".svg")) return "image/svg+xml";
        if (path.endsWith(".woff2")) return "font/woff2";
        if (path.endsWith(".png")) return "image/png";
        if (path.endsWith(".ttf")) return "font/ttf";
        return "application/octet-stream";
    }
    private void immersive() {
        if (Build.VERSION.SDK_INT >= 30) {
            WindowInsetsController controller = getWindow().getInsetsController();
            if (controller != null) {
                controller.hide(WindowInsets.Type.statusBars() | WindowInsets.Type.navigationBars());
                controller.setSystemBarsBehavior(WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
            }
        } else {
            getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY |
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_FULLSCREEN |
                View.SYSTEM_UI_FLAG_HIDE_NAVIGATION);
        }
    }
    private void pauseGame() {
        if (web != null) web.evaluateJavascript("if(window.emberAndroid)window.emberAndroid.pause();", null);
    }
    @Override protected void onPause() {
        pauseGame();
        if (web != null) { web.onPause(); web.pauseTimers(); }
        super.onPause();
    }
    @Override protected void onResume() {
        super.onResume();
        if (web != null) { web.resumeTimers(); web.onResume(); }
        immersive();
    }
    @Override public void onWindowFocusChanged(boolean focused) {
        super.onWindowFocusChanged(focused);
        if (focused) immersive(); else pauseGame();
    }
    @Override public void onBackPressed() { handleBack(); }
    private void handleBack() {
        if (web == null || exitDialog) return;
        web.evaluateJavascript("window.emberAndroid?window.emberAndroid.back():'exit'", result -> {
            if (!"\"exit\"".equals(result) || isFinishing()) return;
            exitDialog = true;
            new AlertDialog.Builder(this).setTitle("退出代号 No.17？")
                .setMessage("已完成的关卡与设置会保留，当前小节需要重新开始。")
                .setNegativeButton("继续游戏", (dialog, which) -> { exitDialog = false; immersive(); })
                .setPositiveButton("退出", (dialog, which) -> finish())
                .setOnCancelListener(dialog -> { exitDialog = false; immersive(); }).show();
        });
    }
    @Override protected void onDestroy() {
        if (web != null) { web.removeJavascriptInterface("EmberHaptics"); web.stopLoading(); web.destroy(); web = null; }
        super.onDestroy();
    }
    public final class Haptics {
        @JavascriptInterface public void vibrate() {
            Vibrator vibrator = (Vibrator)getSystemService(VIBRATOR_SERVICE);
            if (vibrator != null && vibrator.hasVibrator()) vibrator.vibrate(VibrationEffect.createOneShot(45, VibrationEffect.DEFAULT_AMPLITUDE));
        }
    }
}
