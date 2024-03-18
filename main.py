import flet as ft
import asyncio,threading




def main(page: ft.Page):
    page.playback=False
    page.duration=0
    page.current_position=0
    page.current_position_text_value="00:00"
    page.current_position_text_inverted_mode=0

    def upadate_controls(_):
        page.current_position=audio.get_current_position()
        page.duration=audio.get_duration()

        seek_sldr.value=page.current_position
        seek_sldr.max=page.duration

        if page.current_position_text_inverted_mode:
            page.current_position=page.duration-page.current_position
            page.current_position_text_value=f"-{('00'+str(page.current_position//1000//60))[-2:]}:{('00'+str(page.current_position//1000%60))[-2:]}"
        else:
            page.current_position_text_value=f"{('00'+str(page.current_position//1000//60))[-2:]}:{('00'+str(page.current_position//1000%60))[-2:]}"
        current_position_text.text=page.current_position_text_value


        page.update()

    def invert_current_position_text(_):
        page.current_position_text_inverted_mode=1-page.current_position_text_inverted_mode
        if page.current_position_text_inverted_mode:
            page.current_position=page.duration-page.current_position
            page.current_position_text_value=f"-{('00'+str(page.current_position//1000//60))[-2:]}:{('00'+str(page.current_position//1000%60))[-2:]}"
        else:
            page.current_position_text_value=f"{('00'+str(page.current_position//1000//60))[-2:]}:{('00'+str(page.current_position//1000%60))[-2:]}"
        current_position_text.text=page.current_position_text_value

        page.update()

    def playbtn_clk(_):
        if page.playback:
            page.playback=False
            audio.pause()
            playbtn.icon=ft.icons.PLAY_CIRCLE
        else:
            page.playback=True
            audio.resume()
            playbtn.icon=ft.icons.PAUSE_CIRCLE
        page.update()
    
    def seek_sldr_change(_):
        audio.seek(int(seek_sldr.value))
        audio.update()

    def volume_sldr_change(_):
        audio.volume=volume_sldr.value
        audio.update()

    audio = ft.Audio(
        src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
        autoplay=False,
        on_state_changed=upadate_controls,
        on_position_changed=upadate_controls,
        volume=.1,
    )

    seek_sldr=ft.Slider(
        min=0,
        max=page.duration,
        on_change=seek_sldr_change,
        expand=1,
        thumb_color=ft.colors.ORANGE,
        active_color=ft.colors.ORANGE,
    )

    playbtn=ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE,
        on_click=playbtn_clk,
        expand=1,
        icon_color=ft.colors.ORANGE,
    )

    current_position_text=ft.TextButton(
        text=page.current_position_text_value,
        on_click=invert_current_position_text,
        expand=1,
        style=ft.ButtonStyle(
            color=ft.colors.ORANGE,
        )
    )

    volume_sldr=ft.Slider(
        min=0,
        max=1,
        value=.1,
        on_change=volume_sldr_change,
        expand=2,
        thumb_color=ft.colors.ORANGE,
        active_color=ft.colors.ORANGE,
    )


    page.overlay.append(audio)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[ft.Container(
                padding=2,
                border_radius=ft.border_radius.all(20),
                bgcolor=ft.colors.BLACK,
                width=300,
                content=ft.Column(controls=[
                    ft.Row([
                        seek_sldr,
                    ]),
                    ft.Row([
                        playbtn,
                        current_position_text,
                        volume_sldr   
                    ])
                ])
            )]
        )
    )
    #page.on_resize=lambda _:page.update()




if __name__=="__main__":
    ft.app(target=main, port=1234, view=ft.AppView.WEB_BROWSER)