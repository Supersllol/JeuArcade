from __future__ import annotations

import os
import sys
import pygame
import math
from AA.AA_scenes import homeScene
from AA.AA_scenes.sceneClass import Scene
from AA.AA_utils import inputManager, musicManager, settings, dbManager, misc, fontManager


class RankingsScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 dbManager: dbManager.DatabaseManager):
        super().__init__(mainApp, inputManager, musicManager, dbManager)

        # Load background and scale to window
        self.bg_image = pygame.image.load(
            os.path.join(settings.PARENT_PATH, "AA_images",
                         "dojo.jpg")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               settings.WINDOW_SIZE).convert()

        self._icons = {
            "select":
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images",
                             "AA_input_instruction", "Quitter - Select.png")),
        }
        # Scale input icons uniformly
        for key, img in list(self._icons.items()):
            self._icons[key] = pygame.transform.scale(
                img, (150, 50)).convert_alpha()

        self.rankingsBg = misc.rescaleSurface(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images",
                             "fond_rankings.png")), (None, 610))

    def initScene(self):
        rankings = self._dbManager.getRecordOrder()
        if len(rankings) == 0:
            txt = fontManager.upheaval("Aucune donnée disponible", 40,
                                       (255, 255, 255))
            self.rankingsBg.blit(
                txt, txt.get_rect(center=self.rankingsBg.get_rect().center))
        else:
            # Layout column x positions (relative to the left edge of rankingsBg)
            colX = [160, 290, 440, 610]
            # Draw table headers
            header_y = 100
            header_color = (255, 204, 37)
            hdr_rank = fontManager.upheaval("RANG", 36, header_color)
            hdr_name = fontManager.upheaval("NOM", 36, header_color)
            hdr_country = fontManager.upheaval("PAYS", 36, header_color)
            hdr_score = fontManager.upheaval("FICHE", 36, header_color)

            self.rankingsBg.blit(hdr_rank,
                                 hdr_rank.get_rect(center=(colX[0], header_y)))
            self.rankingsBg.blit(hdr_name,
                                 hdr_name.get_rect(center=(colX[1], header_y)))
            self.rankingsBg.blit(
                hdr_country, hdr_country.get_rect(center=(colX[2], header_y)))
            self.rankingsBg.blit(
                hdr_score, hdr_score.get_rect(center=(colX[3], header_y)))

            # Prepare rows: show up to 10 players
            rows = rankings[:10]
            n_rows = 10

            # Vertical layout: place the first row with a top margin,
            # then use different gaps after row 1, rows 2-3, and the rest.
            top_margin = 160
            y = top_margin

            gap_after = {
                1: 60,  # big gap after rank 1
                2: 50,  # medium gap after rank 2
                3: 50  # medium gap after rank 3
            }
            small_gap = 33  # gap after ranks 4..10

            # Fonts sizes for ranks
            font_size = {1: 60, 2: 45, 3: 45}
            default_font_size = 30

            white = (255, 255, 255)

            for idx in range(n_rows):
                # center Y for this row (we use y to position centered text)
                center_y = y

                if idx < len(rows):
                    record = rows[idx]
                    rank_num = idx + 1
                    score_text = f"{record.win} - {record.lose}"

                    # choose font sizes
                    rank_font_size = font_size.get(rank_num, default_font_size)
                    name_font_size = font_size.get(rank_num, default_font_size)

                    rank_font = fontManager.upheaval(str(rank_num),
                                                     rank_font_size, white)
                    name_font = fontManager.upheaval(record.playerName,
                                                     name_font_size, white)
                    country_font = fontManager.upheaval(
                        str(record.playerCountry), name_font_size, white)
                    score_font = fontManager.upheaval(score_text,
                                                      name_font_size, white)

                    # Draw rank (left column)
                    self.rankingsBg.blit(
                        rank_font,
                        rank_font.get_rect(center=(colX[0], center_y)))

                    # Draw name (column 2)
                    self.rankingsBg.blit(
                        name_font,
                        name_font.get_rect(center=(colX[1], center_y)))

                    # Draw country (column 3)
                    self.rankingsBg.blit(
                        country_font,
                        country_font.get_rect(center=(colX[2], center_y)))

                    # Draw wins-losses (column 4 / right-aligned area)
                    self.rankingsBg.blit(
                        score_font,
                        score_font.get_rect(center=(colX[3], center_y)))
                # else: leave blank row

                # advance y by gap depending on the rank just placed
                rank_just_drawn = idx + 1
                step = gap_after.get(rank_just_drawn, small_gap)
                y += step
        super().initScene()

    def loopScene(self, events: list[pygame.event.Event]):
        for i in range(2):
            if inputManager.ButtonInputs.B in self._inputManager.getBtnsPressed(
                    i):
                self.sceneFinished = True

        # Draw background
        self._mainApp.blit(self.bg_image, (0, 0))

        self._mainApp.blit(
            self.rankingsBg,
            self.rankingsBg.get_rect(center=(self._mainApp.get_rect().centerx,
                                             410)))

        self._mainApp.blit(self._icons["select"],
                           (20, settings.WINDOW_SIZE[1] - 60))

        titre = fontManager.upheaval("record mondial", 75, (255, 204, 37))
        self._mainApp.blit(
            titre,
            titre.get_rect(center=(self._mainApp.get_rect().centerx, 60)))

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> Scene | None:
        return homeScene.HomeScene(self._mainApp, self._inputManager,
                                   self._musicManager, self._dbManager)
