import flet as ft
import asyncio,threading


class app():
    def __init__(self) -> None:
        ft.app(target=self.main, port=1234, view=ft.AppView.WEB_BROWSE)

    def main(self,page: ft.Page):
        self.playback=False
        self.duration=0
        self.current_position=0
        self.current_position_text_value="00:00"


        self.page=page
        self.audio = ft.Audio(
            src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
            autoplay=False,
            on_state_changed=self.upadate_controls,
            on_position_changed=self.upadate_controls,
        )

        self.playbtn=ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE,
            on_click=self.playbtn_clk,
            col=1
        )

        self.seek_sldr=ft.Slider(
            min=0,
            max=self.duration,
            on_change=self.seek_sldr_change,
            col=8.5
        )

        self.current_position_text=ft.Text(
            value=self.current_position_text_value,
            width=40
        )

        self.volume_sldr=ft.Slider(
            min=0,
            max=1,
            on_change=self.volume_sldr_change,
            col=2
        )


        self.page.overlay.append(
            self.audio
        )
        page.add(
            ft.ResponsiveRow([
                self.playbtn,
                self.seek_sldr,
            ]),
            ft.ResponsiveRow([
                self.current_position_text,
                self.volume_sldr   
            ])
        )
        page.on_resize=lambda _:page.update()

    def upadate_controls(self,_):
        self.current_position=self.audio.get_current_position()
        self.duration=self.audio.get_duration()

        self.seek_sldr.value=self.current_position
        self.seek_sldr.max=self.duration

        self.current_position_text_value=f"{('00'+str(self.current_position//1000//60))[-2:]}:{('00'+str(self.current_position//1000%60))[-2:]}"
        self.current_position_text.value=self.current_position_text_value

        self.page.update()

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
    
    def seek_sldr_change(self,_):
        self.audio.seek(int(self.seek_sldr.value))
        self.audio.update()

    def volume_sldr_change(self,_):
        self.audio.volume=self.volume_sldr.value
        self.audio.update()
        



if __name__=="__main__":
    app()