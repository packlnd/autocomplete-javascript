import sublime
import sublime_plugin
import os
import re
import functools

class SnippetCommand(sublime_plugin.TextCommand):


    def run(self, edit):
        """Called when the command is run."""
        self.edit = edit

        # Selection to be made later contains the code snippets
        self.selection = ['a','b','c']

        sublime.active_window().show_quick_panel(
            self.selection, self.on_done_call_func(self.selection, self.insert))

    def on_done_call_func(self, choices, func):
        """Return a function which is used with sublime list picking."""
        def on_done(index):
            if index >= 0:
                return func(choices[index])

        return on_done

    def insert(self, choice):
       
        self.view.run_command('snippet_insert_helper', {
            'args': {
                'choice': choice
            }
        })

class SnippetInsertHelperCommand(sublime_plugin.TextCommand):

    def run(self, edit, args):
        choice = args['choice']
        content = choice + ' = 0'
        position = self.view.sel()[0].begin()
        self.view.insert(edit, position, content)