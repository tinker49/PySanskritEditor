import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GObject, Gdk


class SearchDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(
            self,
            "Search",
            parent,
            Gtk.DialogFlags.MODAL,
            buttons=(
                Gtk.STOCK_FIND,
                Gtk.ResponseType.OK,
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
            ),
        )

        self.connect('key_release_event', self.on_key_press_event)
        box = self.get_content_area()

        label = Gtk.Label("Insert text you want to search for:")
        box.add(label)

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.show_all()


class TextViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="TextView Example")

        self.set_default_size(-1, 350)

        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.connect('key_release_event', self.on_key_press_event)

        global switch_val
        switch_val = "Devanagari"

        self.create_textview()
        self.create_toolbar()
        self.create_buttons()

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        self.grid.attach(toolbar, 0, 0, 3, 1)

        button_open = Gtk.ToolButton()
        button_open.set_icon_name("document-open")
        toolbar.insert(button_open, 0)
        button_open.connect("clicked", self.on_open)

        button_save = Gtk.ToolButton()
        button_save.set_icon_name("document-save")
        toolbar.insert(button_save, 1)
        button_save.connect("clicked", self.on_save)

        button_bold = Gtk.ToolButton()
        button_bold.set_icon_name("format-text-bold-symbolic")
        toolbar.insert(button_bold, 2)

        button_italic = Gtk.ToolButton()
        button_italic.set_icon_name("format-text-italic-symbolic")
        toolbar.insert(button_italic, 3)

        button_underline = Gtk.ToolButton()
        button_underline.set_icon_name("format-text-underline-symbolic")
        toolbar.insert(button_underline, 4)

        button_bold.connect("clicked", self.on_button_clicked, self.tag_bold)
        button_italic.connect(
            "clicked", self.on_button_clicked, self.tag_italic)
        button_underline.connect(
            "clicked", self.on_button_clicked, self.tag_underline)

        toolbar.insert(Gtk.SeparatorToolItem(), 3)

        radio_justifyleft = Gtk.RadioToolButton()
        radio_justifyleft.set_icon_name("format-justify-left-symbolic")
        toolbar.insert(radio_justifyleft, 4)

        radio_justifycenter = Gtk.RadioToolButton.new_from_widget(
            radio_justifyleft)
        radio_justifycenter.set_icon_name("format-justify-center-symbolic")
        toolbar.insert(radio_justifycenter, 5)

        radio_justifyright = Gtk.RadioToolButton.new_from_widget(
            radio_justifyleft)
        radio_justifyright.set_icon_name("format-justify-right-symbolic")
        toolbar.insert(radio_justifyright, 6)

        radio_justifyfill = Gtk.RadioToolButton.new_from_widget(
            radio_justifyleft)
        radio_justifyfill.set_icon_name("format-justify-fill-symbolic")
        toolbar.insert(radio_justifyfill, 7)

        radio_justifyleft.connect(
            "toggled", self.on_justify_toggled, Gtk.Justification.LEFT
        )
        radio_justifycenter.connect(
            "toggled", self.on_justify_toggled, Gtk.Justification.CENTER
        )
        radio_justifyright.connect(
            "toggled", self.on_justify_toggled, Gtk.Justification.RIGHT
        )
        radio_justifyfill.connect(
            "toggled", self.on_justify_toggled, Gtk.Justification.FILL
        )

        toolbar.insert(Gtk.SeparatorToolItem(), 8)

        button_clear = Gtk.ToolButton()
        button_clear.set_icon_name("edit-clear-symbolic")
        button_clear.connect("clicked", self.on_clear_clicked)
        toolbar.insert(button_clear, 9)

        toolbar.insert(Gtk.SeparatorToolItem(), 10)

        button_search = Gtk.ToolButton()
        button_search.set_icon_name("system-search-symbolic")
        button_search.connect("clicked", self.on_search_clicked)
        toolbar.insert(button_search, 11)

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        #self.textbuffer.set_text(
        #    "This is some text inside of a Gtk.TextView. "
        #    + "Select text and click one of the buttons 'bold', 'italic', "
        #    + "or 'underline' to modify the text accordingly."
        #)
        self.textbuffer.set_text("" )
        scrolledwindow.add(self.textview)

        self.tag_bold = self.textbuffer.create_tag(
            "bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag(
            "italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag(
            "underline", underline=Pango.Underline.SINGLE
        )
        self.tag_found = self.textbuffer.create_tag(
            "found", background="yellow")


    def on_save(self, event):
        print('save')
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()
        filter.set_name('All files')
        filter.add_pattern('*')
        dialog.add_filter(filter)

        txtFilter = Gtk.FileFilter()
        txtFilter.set_name('Text file')
        txtFilter.add_pattern('*.txt')
        dialog.add_filter(txtFilter)

        #self.add_filters(dialog)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            print(filename, 'selected.')
            buf = self.textbuffer
            text = buf.get_text(buf.get_start_iter(),
                        buf.get_end_iter(),
                        True)
            try:
                 with open(filename, 'w') as f:
                     f.write(text)
                 #open(filename, 'w').write(text)
            except SomeError as err:
                 print('Could not save %s: %s' % (filename, err))
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def on_open(self, event):
        print('save')
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()
        filter.set_name('All files')
        filter.add_pattern('*')
        dialog.add_filter(filter)

        txtFilter = Gtk.FileFilter()
        txtFilter.set_name('Text file')
        txtFilter.add_pattern('*.txt')
        dialog.add_filter(txtFilter)

        #self.add_filters(dialog)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            print(filename, 'selected.')
            buf = self.textbuffer

            try:
                with open(filename, 'r') as f:
                    data = f.read()
                    buf.set_text(data)
                 #open(filename, 'w').write(text)
            except SomeError as err:
                 print('Could not save %s: %s' % (filename, err))
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def create_buttons(self):
        check_editable = Gtk.CheckButton("Editable")
        check_editable.set_active(True)
        check_editable.connect("toggled", self.on_editable_toggled)
        self.grid.attach(check_editable, 0, 2, 1, 1)

        check_cursor = Gtk.CheckButton("Cursor Visible")
        check_cursor.set_active(True)
        check_editable.connect("toggled", self.on_cursor_toggled)
        self.grid.attach_next_to(
            check_cursor, check_editable, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapnone = Gtk.RadioButton.new_with_label_from_widget(
            None, "No Wrapping")
        self.grid.attach(radio_wrapnone, 0, 3, 1, 1)

        radio_wrapchar = Gtk.RadioButton.new_with_label_from_widget(
            radio_wrapnone, "Character Wrapping"
        )
        self.grid.attach_next_to(
            radio_wrapchar, radio_wrapnone, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapword = Gtk.RadioButton.new_with_label_from_widget(
            radio_wrapnone, "Word Wrapping"
        )
        self.grid.attach_next_to(
            radio_wrapword, radio_wrapchar, Gtk.PositionType.RIGHT, 1, 1
        )

        radio_wrapnone.connect(
            "toggled", self.on_wrap_toggled, Gtk.WrapMode.NONE)
        radio_wrapchar.connect(
            "toggled", self.on_wrap_toggled, Gtk.WrapMode.CHAR)
        radio_wrapword.connect(
            "toggled", self.on_wrap_toggled, Gtk.WrapMode.WORD)

        switch = Gtk.Switch()
        switch.connect("notify::active", self.on_switch_activated)
        switch.set_active(False)

        switch = Gtk.Switch()
        switch.connect("notify::active", self.on_switch_activated)
        switch.set_active(True)
        self.grid.attach(switch, 0, 4, 1, 1)

    def on_button_clicked(self, widget, tag):
        bounds = self.textbuffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.textbuffer.apply_tag(tag, start, end)

    def on_clear_clicked(self, widget):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.remove_all_tags(start, end)

    def on_editable_toggled(self, widget):
        self.textview.set_editable(widget.get_active())

    def on_cursor_toggled(self, widget):
        self.textview.set_cursor_visible(widget.get_active())

    def on_wrap_toggled(self, widget, mode):
        self.textview.set_wrap_mode(mode)

    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = "Devanagari"
            #switch_val = "Devanagari"
            # self.textbuffer.insert_at_cursor(u"\u0905")
        else:
            state = "Roman"
            #self.textview.set_editable(True)
            #switch_val = "Roman"
        print("Switch was turned", state)

    def on_key_press_event(self, widget, event):
        """ Check if any of the key in the shortcut ctrl-alt-u is released """
        # ctrl = 65507, alt = 65513, u = 117
        current_switch_val = self.grid.get_child_at(0, 4).get_active()
        current_editable = self.textview.get_editable()
        self.textview.set_editable(False)
        keys = [65507, 65513, 117]
        print(event.keyval)
        print(event.state)
        print(Gdk.keyval_name(event.keyval))
        
        #start = self.textview.get_buffer().cursor-position;
        print(self.textview.get_buffer().get_property("cursor-position"))
        mask = event.state
        
        accel_masks    = (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD1_MASK)
        accel_masks_nonshift    = (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK)
        accel_masks_control    = (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK)
        accel_masks_shift    = (Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK)
        accel_masks_single    = (Gdk.ModifierType.MOD2_MASK)
        accel_masks_alt    = (Gdk.ModifierType.MOD1_MASK | Gdk.ModifierType.MOD2_MASK)
        accel_masks_nonalt    = (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK)
        keyname = Gdk.keyval_name(event.keyval)
        #if current_switch_val and event.keyval in keys:
        #    self.textbuffer.insert_at_cursor(u"\u0905")  # ctrl-alt-u

        if current_switch_val and Gdk.keyval_name(event.keyval)=="Return":
            self.textbuffer.insert_at_cursor(u"\n")  # \n

        if current_switch_val and (keyname=="k") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0915")  # k
        if current_switch_val and (keyname=="K") and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0916")  # shift-k

        if current_switch_val and (keyname=="c") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u091a")  # c
        if current_switch_val and (keyname=="C") and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u091b")  # shift-c

        if current_switch_val and (keyname=="t") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0924")  # t
        if current_switch_val and (keyname=="T")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0925")  # shift-t

        if current_switch_val and (keyname=="t") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u091f")  # alt-t
        if current_switch_val and (keyname=="T") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0920")  # alt-shift-t

        if current_switch_val and (keyname=="p") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u092a")  # p
        if current_switch_val and (keyname=="P") and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u092b")  # shift-p

        if current_switch_val and (keyname=="g") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0917")  # g
        if current_switch_val and (keyname=="G") and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0918")  # shift-g

        if current_switch_val and (keyname=="j") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u091c")  # j
        if current_switch_val and (keyname=="J") and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u091d")  # shift-j

        if current_switch_val and (keyname=="d") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0921")  # d
        if current_switch_val and (keyname=="D")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0922")  # shift-d

        if current_switch_val and (keyname=="d") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0926")  # alt-d
        if current_switch_val and (keyname=="D") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0927")  # alt-shift-d

        if current_switch_val and (keyname=="b") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u092c")  # b
        if current_switch_val and (keyname=="B") and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u092d")  # shift-b

        if current_switch_val and (keyname=="n") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0928")  # n
        if current_switch_val and (keyname=="N")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0923")  # shift-n
        if current_switch_val and (keyname=="N") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u095c")  # alt-shift-n

        if current_switch_val and (keyname=="s") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0938")  # s
        if current_switch_val and (keyname=="S")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0937")  # shift-s
        if current_switch_val and (keyname=="S") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0936")  # alt-shift-s

        if current_switch_val and (keyname=="y") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u092f")  # y
        if current_switch_val and (keyname=="Y") and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u091e")  # shift-y

        if current_switch_val and (keyname=="l") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0932")  # l
        if current_switch_val and (keyname=="L") and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0933")  # shift-l

        if current_switch_val and (keyname=="h") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0939")  # h
        if current_switch_val and (keyname=="H")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0903")  # shift-h

        if current_switch_val and (keyname=="r") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0930")  # r
        if current_switch_val and (keyname=="w") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0935")  # w

        if current_switch_val and (keyname=="m") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u092e")  # m
        if current_switch_val and (keyname=="M")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0902")  # shift-m


        if current_switch_val and (keyname=="1") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0967")  # 1
        if current_switch_val and (keyname=="2") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0968")  # 2
        if current_switch_val and (keyname=="3") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0969")  # 3
        if current_switch_val and (keyname=="4") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u096a")  # 4
        if current_switch_val and (keyname=="5") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u096b")  # 5
        if current_switch_val and (keyname=="6") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u096c")  # 6
        if current_switch_val and (keyname=="7") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u096d")  # 7
        if current_switch_val and (keyname=="8") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u096e")  # 8
        if current_switch_val and (keyname=="9") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u096f")  # 9
        if current_switch_val and (keyname=="0") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0966")  # 0

        if current_switch_val and (keyname=="grave") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u094d")  # ~
        if current_switch_val and (keyname=="asciitilde")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u200d")  # shift-~ zero width joiner u200d

       # u200d zero width non joiner
        if current_switch_val and (keyname=="q") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u200c")  # q zero width non-joiner -zwnj u200c
        if current_switch_val and (keyname=="Q")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u200d")  # shift-q - zero width joiner - zwj u200d


        if current_switch_val and (keyname=="a") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0905")  # a
        if current_switch_val and (keyname=="A")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0906")  # shift-a

        #if current_switch_val and (keyname=="a") and (mask & Gdk.ModifierType.MOD1_MASK):
        #    self.textbuffer.insert_at_cursor(u"\u093e")  # alt-a
        if current_switch_val and (keyname=="A") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u093e")  # alt-shift-a

        if current_switch_val and (keyname=="i") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0907")  # i
        if current_switch_val and (keyname=="I")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0908")  # shift-i

        if current_switch_val and (keyname=="i") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u093f")  # alt-i
        if current_switch_val and (keyname=="I") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0940")  # alt-shift-i

        if current_switch_val and (keyname=="u") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0909")  # u
        if current_switch_val and (keyname=="U")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u090a")  # shift-u

        if current_switch_val and (keyname=="u") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0941")  # alt-u
        if current_switch_val and (keyname=="U") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0942")  # alt-shift-u

        if current_switch_val and (keyname=="e") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u090f")  # e
        if current_switch_val and (keyname=="E")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0910")  # shift-e

        if current_switch_val and (keyname=="e") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0947")  # alt-e
        if current_switch_val and (keyname=="E") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u0948")  # alt-shift-e

        if current_switch_val and (keyname=="o") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0913")  # o
        if current_switch_val and (keyname=="O")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0914")  # shift-o

        if current_switch_val and (keyname=="o") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u094b")  # alt-o
        if current_switch_val and (keyname=="O") and (mask & Gdk.ModifierType.MOD1_MASK):
            self.textbuffer.insert_at_cursor(u"\u094c")  # alt-shift-o

        if current_switch_val and (keyname=="backslash") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u0964")  # \
        if current_switch_val and (keyname=="bar")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u0965")  # shift-\

        if current_switch_val and (keyname=="apostrophe") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u201c")  # 
        if current_switch_val and (keyname=="quotedbl")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u201d")  # shift-

        if current_switch_val and (keyname=="minus") and not (mask & accel_masks):
            self.textbuffer.insert_at_cursor(u"\u2010")  # -
        if current_switch_val and (keyname=="underscore")  and (mask & accel_masks_shift) and not (mask & accel_masks_nonshift):
            self.textbuffer.insert_at_cursor(u"\u093d")  # shift-- avagraha

        if current_switch_val and (keyname=="BackSpace") and not (mask & accel_masks):
            curpos = self.textview.get_buffer().get_property("cursor-position")
            self.textbuffer.delete(self.textview.get_buffer().get_iter_at_offset(curpos-1),self.textview.get_buffer().get_iter_at_offset(curpos))  # -


    def on_justify_toggled(self, widget, justification):
        self.textview.set_justification(justification)

    def on_search_clicked(self, widget):
        dialog = SearchDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cursor_mark = self.textbuffer.get_insert()
            start = self.textbuffer.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.textbuffer.get_char_count():
                start = self.textbuffer.get_start_iter()

            self.search_and_mark(dialog.entry.get_text(), start)

        dialog.destroy()

    def search_and_mark(self, text, start):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match is not None:
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(text, match_end)


win = TextViewWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
