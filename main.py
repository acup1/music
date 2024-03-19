import flet as ft


def main(page: ft.Page):
    page.playback=False
    page.duration=0
    page.current_position=0
    page.current_position_text_value="00:00"
    page.duration_timeformat="00:00"
    page.current_position_text_inverted_mode=0
    page.accent_color=ft.colors.WHITE

    def upadate_controls(_):
        page.current_position=audio.get_current_position()
        page.duration=audio.get_duration()

        seek_sldr.value=page.current_position
        seek_sldr.max=page.duration
        update_time()        

    def update_time():
        page.duration_timeformat=f"{('00'+str(page.duration//1000//60))[-2:]}:{('00'+str(page.duration//1000%60))[-2:]}"
        if page.current_position_text_inverted_mode:
            page.current_position=page.duration-page.current_position
            page.current_position_text_value=f"-{('00'+str(page.current_position//1000//60))[-2:]}:{('00'+str(page.current_position//1000%60))[-2:]}"
        else:
            page.current_position_text_value=f"{('00'+str(page.current_position//1000//60))[-2:]}:{('00'+str(page.current_position//1000%60))[-2:]}"
        current_position_text.text=page.current_position_text_value+"/"+page.duration_timeformat
        page.update()


    def invert_current_position_text(_):
        page.current_position_text_inverted_mode=1-page.current_position_text_inverted_mode
        update_time()

        page.update()

    def playbtn_clk(_=None):
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

    def on_keyboard(e: ft.KeyboardEvent):
        #print(e.key)
        if e.key==" ":
            playbtn_clk()
        elif e.key=="Arrow Right":
            audio.seek(int(min(seek_sldr.value+10000,page.duration-1)))
            audio.update()
        elif e.key=="Arrow Left":
            audio.seek(int(max(seek_sldr.value-10000,0)))
            audio.update()

    page.on_keyboard_event = on_keyboard    

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
        text="--:--/--:--",
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

    page.bottom_appbar=ft.BottomAppBar(content=ft.ResponsiveRow(
        #vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                padding=2,
                border_radius=ft.border_radius.all(20),
                bgcolor=ft.colors.BLACK,
                col=12,
                content=ft.Column(controls=[
                    ft.Row([
                        seek_sldr,
                    ]),
                ])
            ),
            ft.Container(
                padding=2,
                border_radius=ft.border_radius.all(20),
                bgcolor=ft.colors.BLACK,
                col=12,
                content=ft.Column(controls=[
                    ft.Row([
                        ft.Column([
                                current_position_text,
                            ],
                            expand=7,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Column([
                                playbtn,
                            ],
                            expand=4,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(expand=1,content=ft.Text("")),
                        ft.Column([
                                volume_sldr,
                            ],
                            expand=4,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ])
                ])
            ),
        ]
    ))
    page.add(ft.Text("Body!"))
    #page.on_resize=lambda _:page.update()




if __name__=="__main__":
    ft.app(target=main, port=1234, view=ft.AppView.WEB_BROWSER)