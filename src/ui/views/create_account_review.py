from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING

from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from misc.api_models import UCSD_EMAIL_DOMAIN as EMAIL_DOMAIN
from misc.global_context import context
from ui.base import Screen
from ui.components.styled_button import StyledButton
from ui.components.label import field_label
from ui.components.styled_entry import StyledEntry, field_row
from ui.theme import ERROR

if TYPE_CHECKING:
    from controllers.navigation_controller import NavigationController

EMAIL_MISMATCH_TEXT = "Emails don't match"


class CreateAccountReview(Screen):
    def _build(self, controller: NavigationController) -> None:
        self.add_home_row()

        self.content.addSpacing(8)

        self.first_name_entry = field_row(self.content, "First Name")
        self.last_name_entry = field_row(self.content, "Last Name")
        self.email_entry = field_row(self.content, "School Email")

        self.confirm_email_container = QWidget()
        confirm_layout = QVBoxLayout(self.confirm_email_container)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        confirm_layout.setSpacing(0)
        self.confirm_email_entry = field_row(confirm_layout, "Confirm School Email")
        # text is toggled rather than the label hidden so the layout doesn't jump
        self.email_mismatch_label = field_label(EMAIL_MISMATCH_TEXT)
        self.email_mismatch_label.setStyleSheet(f"color: {ERROR}")
        self.email_mismatch_label.setText("")
        confirm_layout.addWidget(self.email_mismatch_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.content.addWidget(self.confirm_email_container)

        # since the email is being prepended there should never be a "@" typed in. emails also shouldn't contain spaces
        self._username_validator = QRegularExpressionValidator(QRegularExpression(r"[^@\s]*"), self)

        self.pid_container = QWidget()
        pid_layout = QVBoxLayout(self.pid_container)
        pid_layout.setContentsMargins(0, 0, 0, 0)
        pid_layout.setSpacing(0)
        self.pid_entry = field_row(pid_layout, "PID")
        self.content.addWidget(self.pid_container)

        self._is_manual = True

        for entry in self._entries():
            entry.returnPressed.connect(lambda e=entry: self._advance(e))
            entry.textChanged.connect(self._update_btn_state)
            entry.textChanged.connect(self._update_tap_hints)
            entry.focus_changed.connect(self._update_tap_hints)
        self.confirm_email_entry.editingFinished.connect(self._update_btn_state)

        self.content.addStretch(1)

        btn_row = QHBoxLayout()
        self.continue_btn = StyledButton("Continue")
        self.continue_btn.setFixedWidth(349)
        self.continue_btn.setEnabled(False)
        self.continue_btn.clicked.connect(self._submit)
        btn_row.addStretch()
        btn_row.addWidget(self.continue_btn)
        btn_row.addStretch()
        self.content.addLayout(btn_row)

    def _entries(self) -> tuple[StyledEntry, ...]:
        return (self.first_name_entry, self.last_name_entry, self.email_entry,
                self.confirm_email_entry, self.pid_entry)

    def _required_entries(self) -> list[StyledEntry]:
        entries = [self.first_name_entry, self.last_name_entry, self.email_entry]
        if self._is_manual:
            entries.append(self.confirm_email_entry)
        else:
            entries.append(self.pid_entry)
        return entries

    def _editable_entries(self) -> list[StyledEntry]:
        return [e for e in self._required_entries() if not e.isReadOnly()]

    def _advance(self, current: StyledEntry) -> None:
        editable = self._editable_entries()
        if current not in editable or current is editable[-1]:
            self._submit()
            return
        editable[editable.index(current) + 1].setFocus()

    def _update_tap_hints(self) -> None:
        editable = self._editable_entries()

        focused_index = -1
        for i, entry in enumerate(editable):
            if entry.hasFocus():
                focused_index = i
                break

        upcoming = None
        for i, entry in enumerate(editable):
            if i <= focused_index:
                continue
            if not entry.text().strip():
                upcoming = entry
                break

        for entry in self._entries():
            entry.set_tap_hint_enabled(entry is upcoming)

    def _emails_mismatch(self) -> bool:
        email = self._username(self.email_entry.text())
        confirm = self._username(self.confirm_email_entry.text())
        if not confirm:
            return False
        if self.confirm_email_entry.hasFocus():
            # still typing: only flag once it can no longer match
            return not email.startswith(confirm)
        return confirm != email

    def _update_btn_state(self) -> None:
        filled = all(e.text().strip() for e in self._required_entries())
        if not self._is_manual:
            self.continue_btn.setEnabled(filled)
            return

        mismatch = self._emails_mismatch()
        self.confirm_email_entry.set_error(mismatch)
        self.email_mismatch_label.setText(EMAIL_MISMATCH_TEXT if mismatch else "")
        emails_equal = self._username(self.email_entry.text()) == self._username(self.confirm_email_entry.text())
        self.continue_btn.setEnabled(filled and emails_equal)

    def on_show(self) -> None:
        session = context().session
        self._is_manual = not session.pid

        for entry in (self.email_entry, self.confirm_email_entry):
            entry.setValidator(self._username_validator if self._is_manual else None)
            entry.set_suffix(EMAIL_DOMAIN if self._is_manual else None)

        self.first_name_entry.setText(session.first_name)
        self.last_name_entry.setText(session.last_name)
        self.email_entry.setText(session.email)
        self.confirm_email_container.setVisible(self._is_manual)
        self.pid_container.setVisible(not self._is_manual)
        if not self._is_manual:
            self.pid_entry.setText(session.pid.upper())
            self.pid_entry.set_readonly(True)
        self._update_btn_state()
        self.first_name_entry.setFocus()
        self._update_tap_hints()

    def on_hide(self) -> None:
        for entry in self._entries():
            entry.clearFocus()
        self.clear_entries()

    def clear_entries(self) -> None:
        for entry in self._entries():
            entry.clear()
        self.pid_entry.set_readonly(False)

    @staticmethod
    def _username(text: str) -> str:
        return text.strip().lower()

    def _submit(self) -> None:
        if not all(e.text().strip() for e in self._required_entries()):
            return

        first = self.first_name_entry.text().strip()
        last = self.last_name_entry.text().strip()

        if self._is_manual:
            username = self._username(self.email_entry.text())
            if not username:
                return
            if username != self._username(self.confirm_email_entry.text()):
                return
            email = username + EMAIL_DOMAIN
            pid = None
        else:
            email = self.email_entry.text().strip()
            pid = self.pid_entry.text().strip().upper()

        self.clear_entries()

        def worker() -> None:
            success = context().account_controller.create_account(
                first_name=first, last_name=last, email=email, pid=pid
            )
            if success:
                context().check_in_controller.check_in(
                    "rfid",
                    context().session.rfid,
                    welcome_message="Thank you for registering",
                )
            else:
                context().main_window.main_thread_dispatcher.emit(
                    context().navigation_controller.reset_check_in_session
                )

        Thread(target=worker, daemon=True).start()
