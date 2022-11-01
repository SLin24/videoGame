import sprites
import settings
platforms = []
platforms.append(sprites.TempPlatform(settings.screen, 1300, 200, 100))
platforms.append(sprites.TempPlatform(settings.screen, 1500, 100, 100))
platforms.append(sprites.TempPlatform(settings.screen, 1700, 0, 100))
platforms.append(sprites.Platform(settings.screen, 300, 500, 300))
platforms.append(sprites.Platform(settings.screen, 700, 450, 300))
platforms.append(sprites.Platform(settings.screen, 900, 300, 400))
platforms.append(sprites.Platform(settings.screen, 600, 200, 200))
platforms.append(sprites.EndPlatform(settings.screen, 2000, 400, 200))


# sorting based on height to make sure the loop checks for the ground in the correct order 
platforms = sorted(platforms, key = lambda x: x.y)
platforms.reverse()