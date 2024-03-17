import flet as ft
import asyncio, threading

class app():
    def __init__(self):
        self.playback=False
        ft.app(target=self.main)

    async def main(self,page: ft.Page):
        self.page=page
        self.audio = ft.Audio(
            src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
            autoplay=False
        )

        self.playbtn=ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE,
            on_click=self.playbtn_clk
        )

        self.volume_sldr=ft.Slider(
            min=0,
            max=1,
            on_change=self.volume_sldr_change,
            width=page.window_width*0.3
        )

        await page.add_async(
            self.audio,
            ft.Row([
                    self.playbtn,
                    self.volume_sldr   
            ])
        )
        page.on_resize=lambda _:page.update()

    def playbtn_clk(self,_):
        if self.playback:
            self.playback=False
            self.audio.pause()
            self.playbtn.icon=ft.icons.PLAY_CIRCLE
        else:
            self.playback=True
            self.audio.resume()
            self.playbtn.icon=ft.icons.PAUSE_CIRCLE
        self.page.update()
    
    def volume_sldr_change(self,_):
        self.audio.volume=self.volume_sldr.value
        self.audio.update()
        

if __name__=="__main__":
    app()