# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from koach import query
import neovim


@neovim.plugin
class KoachPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('Koach', range='', nargs='*')
    def visual_mode_koach(self, args, range):
        # start_line = self.nvim.eval('line("\'<")')
        # end_line = self.nvim.eval('line("\'>")')
        start_line, end_line = range

        content = self.nvim.current.buffer[start_line-1:end_line]
        buf = self.ensure_buffer('_koach_output')
        self.clear_buffer(buf)
        content_str = '\n'.join([l.decode('utf-8') for l in content])
        result = query(content_str)

        result_str = ''
        for item in result:
            result_str += '{0}  ->  {1}\n{2}\n\n'.format(
                item['word'], ', '.join(item['replaces']), item['help'])
        output = '{0}\n\n-----------\n\n{1}'.format(content_str, result_str)
        self.append_text_to_buffer(buf, output)

    def ensure_buffer(self, name):
        # return buffer if exists
        bufs = [b for b in self.nvim.buffers if b.name == name]
        if bufs:
            # choose first one
            buf = bufs[0]
            # re-open buffer
            if not any(list(self.nvim.windows),
                       lambda x: x.buffer.name == name):
                self.nvim.command('set splitright')
                self.nvim.command('buffer {0}'.format(name))
                # set instant scratch buffer
                self.nvim.command('setlocal buftype=nofile bufhidden=delete '
                                  'noswapfile')
            return buf
        # create new buffer
        self.nvim.command('set splitright')
        self.nvim.command('vnew')
        buf = self.nvim.current.buffer
        buf.name = name
        # set instant scratch buffer
        self.nvim.command('setlocal buftype=nofile bufhidden=delete '
                          'noswapfile')
        return buf

    def clear_buffer(self, buf):
        buf[:] = []

    def append_text_to_buffer(self, buf, text):
        lines = text.splitlines()
        buf[len(buf):] = lines
