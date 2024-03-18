import flet as ft
import asyncio,threading




def main(page: ft.Page):
    page.playback=False
    page.duration=0
    page.current_position=0
    page.current_position_text_value="00:00"
    page.current_position_text_inverted_mode=0
    page.accent_color=ft.colors.WHITE

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
        thumb_color=page.accent_color,
        active_color=page.accent_color,
    )

    playbtn=ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE,
        on_click=playbtn_clk,
        col=1,
        icon_color=page.accent_color,
    )

    current_position_text=ft.TextButton(
        text=page.current_position_text_value,
        on_click=invert_current_position_text,
        col=2,
        style=ft.ButtonStyle(
            color=page.accent_color,
        )
    )

    volume_sldr=ft.Slider(
        min=0,
        max=1,
        value=.1,
        on_change=volume_sldr_change,
        col=3,
        thumb_color=page.accent_color,
        active_color=page.accent_color,
    )


    page.overlay.append(audio)

    page.add(
        ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[ft.Container(
                padding=2,
                border_radius=ft.border_radius.all(20),
                bgcolor=ft.colors.BLACK,
                col=12,
                content=ft.Column(controls=[
                    ft.Row([
                        seek_sldr,
                    ]),
                    ft.ResponsiveRow([
                        ft.Column([
                                playbtn,
                            ],
                            col=1,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Column([
                            current_position_text,
                            ],
                            col=1,
                        ),
                        ft.Column([
                            volume_sldr,
                            ],
                            col=3,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ])
                ])
            )]
        )
    )
    #page.on_resize=lambda _:page.update()




if __name__=="__main__":
    ft.app(target=main, port=1234, view=ft.AppView.WEB_BROWSER)