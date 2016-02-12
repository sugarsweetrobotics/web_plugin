
@HtmlImport('app-template.html')
library app_template;

import 'dart:html' as html;
import 'package:web_components/web_components.dart' show HtmlImport;
import 'package:polymer/polymer.dart';

import 'package:wasanbon_elements/wasanbon_toolbar.dart';
import 'package:wasanbon_elements/message_dialog.dart';

@PolymerRegister('app-template')
class AppTemplate extends PolymerElement {

  AppTemplate.created() : super.created();

  void attached() {
    $$('#toolbar').onBack = this.onBack;
  }

  @reflectable
  void onBack(var e, var d) {
    ConfirmDialog dlg = $$('#message-dlg');
    dlg.eventListener.ok.add((var dlg_) {
      html.window.location.assign('http://${Uri.base.host}:${Uri.base.port}');
    });
    dlg.show('Confirm', 'Really exit from Setting Manager?');
  }
}
