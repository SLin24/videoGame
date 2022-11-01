import sprites
import settings
platforms = []
platforms.append(sprites.Platform(settings.screen, 300, 600, 300))
platforms.append(sprites.Platform(settings.screen, 300, 2000, 200))
platforms.append(sprites.Platform(settings.screen, 700, 500, 400))
platforms.append(sprites.Platform(settings.screen, 1250, 600, 200))
platforms.append(sprites.Platform(settings.screen, -100, 2000, 200))
platforms.append(sprites.Platform(settings.screen, -500, 2000, 200))
platforms.append(sprites.Platform(settings.screen, -850, 1900, 200))
platforms.append(sprites.Platform(settings.screen, 1100, 750, 200))
platforms.append(sprites.Platform(settings.screen, 1300, 700, 50))

platforms.append(sprites.TempPlatform(settings.screen, -950, 1750, 50))
platforms.append(sprites.TempPlatform(settings.screen, -850, 1650, 50))
platforms.append(sprites.TempPlatform(settings.screen, -850, 1500, 50))
platforms.append(sprites.TempPlatform(settings.screen, -1000, 1500, 50))
platforms.append(sprites.TempPlatform(settings.screen, -1125, 1370, 50))
platforms.append(sprites.TempPlatform(settings.screen, -1030, 1250, 50))
platforms.append(sprites.TempPlatform(settings.screen, -950, 1125, 50))
platforms.append(sprites.TempPlatform(settings.screen, -775, 1050, 50))
platforms.append(sprites.TempPlatform(settings.screen, -675, 900, 50))

platforms.append(sprites.EndPlatform(settings.screen, -400, 1300, 100))


# sorting based on height to make sure the loop checks for the ground in the correct order 
platforms = sorted(platforms, key = lambda x: x.y)
platforms.reverse()
